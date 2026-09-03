# Source notes — 2026-08-27, Series 4 Winter

## Защищённый внеплановый запуск — 2026-09-03 06:58 +07:00

- RunId: `fh6-20260903-065612-941360`. После внедрения трёх уровней защиты повторно проверены все 16 обязательных источников и каждый из 14 визуалов. Данные активной Winter подтверждены официальной Playlist; Spring в таблице — предстоящий сезон. Дедлайн: 03.09.2026 21:30 Красноярск, 53 очка. Сводка актуальна по доступным источникам — содержательных изменений не требуется; успешная пересборка ещё не заявляется.
- Изображения: AutoZOOM, CultClassic, Ohtani, Micro Circuits, Modern Marvels, Edamame Time Attack, Shirakawa-go, Highland Road, Matsumi Curve, Vision Chaser, Drift Tandem, Mini Games и Edamame Circuit сопоставлены с отдельными изображениями текущей Winter на ForzaLabs. Daily отдельно проверен по Fandom, ForzaLabs, Reddit и поиску: подходящего нового изображения нет. Все 14 локальных файлов существуют; их SHA-256 зарегистрированы в локальном аудите запуска. `confirmed=13; community=0; preliminary=1; missing=0`, `openItems=1` (Daily visual). Изображения прошлой недели не переносились.
- Условия и уже опубликованные share codes вновь сверены с текущенедельными гайдами; новых обязательных поправок не найдено. Советы сообщества не тестировались в игре. Расхождения официальной веб-таблицы по Matsumi Curve и награде Treasure остаются учтёнными в предыдущем разделе.
- Проверка защит: 21 локальный тест журнала/контрольных этапов/повторной доставки прошёл; пять сценариев watchdog прошли в настоящем шаблонизаторе HA без тестовых тревог. Сохранены резервные копии двух затрагиваемых конфигураций HA, `check_config=valid`. Расписание Codex осталось 06:00; независимый контроль HA — 06:30 и повторная проверка каждые 5 минут, максимум одна тревога в день.
- Наличие обязательного legacy-сборщика проверяет preflight нового конвейера до изменения timestamp. При его отсутствии остаётся BLOCKED; публикация допускается только для инструкций/кода/аудита с неизменными ранее проверенными файлами отчёта. Поддельный результат штатной проверки не создаётся.

| Источник | Проверка в этом запуске |
|---|---|
| fandom_series_category | [Category:Series (FH6)](https://forza.fandom.com/wiki/Category:Series_(FH6)) через MediaWiki API: страницы Series 1–4 и категория Series 5. |
| fandom_current | [Winter Season](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Winter_Season) через API: revision 170723, 53 очка, галерея без Daily. |
| forza_playlist | [Живая Playlist](https://forza.net/fh6playlists): Winter 27.08–03.09; Spring предварительно есть в таблице, rollover не подтверждён. |
| forza_news | News, [Series 4](https://forza.net/news/forza-horizon-6-series-4), [Drift Attack](https://forza.net/news/forza-horizon-6-drift-attack): анонсы сентября не меняют текущую Winter. |
| forza_support_release_notes | Секция недоступна; в отличие от предыдущей попытки, [прямая статья 24.08](https://support.forza.net/hc/en-us/articles/54674846729875-FH6-Release-Notes-August-24-2026) открылась. Исправления дорожного прогресса и доступа к винилам не меняют карточки Winter. |
| forza_support_known_issues | [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) доступна; полный Feedback Portal за авторизацией по-прежнему не проверен. |
| forza_forums_official | [Official-info](https://forums.forza.net/tag/official-info/1731) перенаправляет на закрытые форумы; текущего форумного материала нет. |
| reddit_forzahorizon | [Winter tuning guide](https://www.reddit.com/r/ForzaHorizon/comments/1w1q972/fh6_series_4_winter_tuning_guide/) и breakdown текущей недели доступны; новых обязательных исправлений не установлено. |
| reddit_forzahorizon6 | [Winter guide](https://www.reddit.com/r/ForzaHorizon6/comments/1vzu6tb/fh6_series_4_winter_festival_playlist_guide/) и [Seasonal Tunes](https://www.reddit.com/r/ForzaHorizon6/comments/1vzvho1/seasonal_tunes_by_awes0me_beau/) повторно проверены; текущие рекомендации сохранены. |
| reddit_forza | [Winter Information Thread](https://www.reddit.com/r/forza/comments/1vzy764/fh6_winter_information_thread_series_4/) подтверждает 53 очка и смену 03.09 14:30 UTC. |
| reddit_forzatune | [Лента](https://www.reddit.com/r/ForzaTune/new/) и адресный поиск проверены; свежего соответствующего FH6 Winter материала в доступном индексе не найдено. |
| forza_horizon_hub | [Hub](https://forzahorizonhub.com/) доступен, 632 машины; сезонный блок по-прежнему Series 1, не использован как источник текущей недели. |
| forza_labs_collector | [Collector](https://forza.labsgg.com/collector-tool): веб-чтение не сработало, прямой HTTP 200; каталог 628 машин. Нового решения для текущих пробелов нет. |
| forza_labs_map | [Карта](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) доступны; 13 отдельных текущих плиток, Daily отсутствует. |
| escorenews_fh6 | Категория недоступна; [гайд Winter от 27.08](https://escorenews.com/ru/article/80714-polnyj-gayd-na-ispytaniya-festivalya-v-zimniy-sezon-seriya-4-v-forza-horizon-6-luchshie-mashiny-i-tyuning) доступен. Основания менять опубликованные карточки не получены. |
| dungg_playlist | [Плейлист](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) недоступен; адресный поиск не подтвердил выпуск текущей недели. Старые видео не использованы. |

## Внеплановая проверка — 2026-09-03 06:37 +07:00

- Режим: повтор после незавершённого утреннего heartbeat. Все 16 обязательных источников проверены открытием или адресным поиском; недоступность и отсутствие свежего материала перечислены ниже. Живая [официальная Playlist](https://forza.net/fh6playlists) всё ещё озаглавлена Winter (27 августа — 3 сентября); Spring уже есть в таблице как предстоящая неделя. [ForzaLabs](https://forza.labsgg.com/series/details) выбирает Winter и помечает Spring закрытым. До сброса 3 сентября в 21:30 Asia/Krasnoyarsk rollover не выполнялся.
- Сводка актуальна по доступным подтверждениям — содержательных изменений карточек не требуется. Сохраняются 14 карточек, один Daily из 7 заданий и 53 очка за неделю. Проверенные текущенедельные источники не дали основания заменять рекомендации или share codes; проверка в игре не выполнялась.
- Аудит всех 14 visual: локальные файлы существуют, SHA-256 различны; точные текущенедельные изображения 13 недневных активностей по-прежнему доступны на ForzaLabs. Итог: `confirmed=13`, `community=0`, `preliminary=1`, `missing=0`. У объединённого Daily остаётся временное изображение и `openItems=1`: отдельной текущенедельной плитки в Fandom/ForzaLabs и доступном поиске не найдено. Новая найденная страница ForzaFactory по Horizon Story не читается; её изображения не использовались.
- Расхождения источников: официальная веб-таблица продолжает показывать Matsumi Curve 70 mph вместо 75 mph на игровой плитке, Fandom и Reddit; для Treasure она показывает Super Wheelspin вместо 100 000 CR на плитке ForzaLabs, Fandom и текущенедельном Reddit. Существующие значения 75 mph и 100 000 CR сохранены, конфликт веб-таблицы зафиксирован здесь.
- **Сборка BLOCKED:** в установленном Data Analytics `0.2.35-13ceeea1f599` отсутствует обязательный `deliver_portable_artifact.mjs`; поиск точного файла в локальных кэшах plugins и .cache не дал результата. Новый skill использует другой Data App pipeline. Подмена штатной проверки или миграция структуры не выполнялись. `lastContentUpdate` и производные HTML/JSON/Markdown не изменены; на публичной странице остаётся `2026-09-02T06:04:59+07:00`. Это не полностью успешное обновление.
- Проверка прежней публикации выполнена штатным publisher без нового коммита: `STRUCTURE_OK cards=14 open_items=1`, `PUBLISHED_SHA=66c50bf5965266a0a1b18133909b541fb59d2718`, HTML 45 515 байт; GitHub Pages и относительные изображения доступны. Steam пересобран без содержательных изменений: 4093/4800 символов, `STEAM_STATUS=UP_TO_DATE`, `STEAM_VERIFICATION=PUBLIC_AND_LOCAL`. Публичный Steam не редактировался. Этот датированный аудит оставлен локально до восстановления сборочного конвейера.
- Статистика получена отдельно от заблокированной сборки: `PUBLIC_METRICS_STATUS=OK`, RunId `2026-09-03T06:37:57+07:00-manual-blocked`. Steam: 565 просмотров (+60), 29 в избранном (+3); GitHub-сводка: 554 просмотра (+123) относительно предыдущего успешного снимка метрик. Итоговое уведомление с этими числами отправлено один раз: `HA_NOTIFICATION_STATUS=SENT`, `HA_NOTIFICATION_TYPE=CheckBlocked`, тот же RunId. Полный цикл обновления не объявляется успешным.

| Обязательный источник | Результат |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: страницы Series 1–4, категория Series 5 без страницы новой серии. |
| Forza Wiki / Fandom | Winter revision `170723`, 29.08.2026 17:25:11 UTC; период 27.08–03.09, 53 очка и условия сохранены; в галерее нет Daily-плитки. |
| Official Forza Festival Playlist | Winter подтверждён; Spring предварительно опубликована, но новый активный сезон ещё не наступил. Два расхождения награды/скорости отмечены выше. |
| Official Forza News | Проверены News, [Series 4](https://forza.net/news/forza-horizon-6-series-4) и [Drift Attack](https://forza.net/news/forza-horizon-6-drift-attack): следующая версия игры 7 сентября, British Automotive с 10 сентября; это не текущий rollover. |
| Forza Support Release Notes | Секция и прямая статья 24 августа недоступны через веб-чтение; доступный список связанных статей Known Issues по-прежнему указывает последним патч 24.08. Более нового подтверждения не получено. |
| Forza Support Known Issues | Страница доступна, обновлена 20 июля и отсылает в Feedback Portal; актуальный список за входом Atlassian не проверен. Отсутствие новых багов не гарантируется. |
| Official Forza Forums | Перенаправление на страницу закрытых форумов; нового форумного источника текущей недели нет. |
| Reddit r/ForzaHorizon | Найдены текущие [breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1vzu2vc/fh6_series_4_winter_breakdown_and_rewards/) от 27.08 и [tuning guide](https://www.reddit.com/r/ForzaHorizon/comments/1w1q972/fh6_series_4_winter_tuning_guide/) от 29.08; свежей обязательной замены текущих рекомендаций не установлено. |
| Reddit r/ForzaHorizon6 | [Полный Winter guide](https://www.reddit.com/r/ForzaHorizon6/comments/1vzu6tb/fh6_series_4_winter_festival_playlist_guide/) подтверждает текущие Autozam/Subaru/BMW/PR-коды; [Awes0me Beau](https://www.reddit.com/r/ForzaHorizon6/comments/1vzvho1/seasonal_tunes_by_awes0me_beau/) подтверждает Honda Beat 120 569 217 и Skyline 560 632 810. Отдельной Daily-плитки нет. |
| Reddit r/forza | [Winter Information Thread](https://www.reddit.com/r/forza/comments/1vzy764/fh6_winter_information_thread_series_4/) от 27.08 с ответом 02.09 подтверждает дедлайн 03.09 14:30 UTC; новых поправок к карточкам не найдено. |
| Reddit r/ForzaTune | Адресный поиск FH6/Winter текущей недели не нашёл соответствующего материала в этом subreddit. Это отсутствие в доступном индексе, а не подтверждение полного отсутствия публикаций. |
| Forza Horizon Hub | Доступен, 632 машины; недельный блок всё ещё Series 1, поэтому не использован для текущей Winter. |
| ForzaLabs Collector Tool | Доступен каталог 628 автомобилей; новой информации по Daily-визуалу нет. |
| ForzaLabs Interactive Map | Страница карты доступна; нового подтверждённого сезонного маркера/решения не получено. Дополнительно проверена Series Details со всеми 13 текущими плитками. |
| Escorenews FH6 | Категория недоступна; [Winter guide от 27.08](https://escorenews.com/ru/article/80714-polnyj-gayd-na-ispytaniya-festivalya-v-zimniy-sezon-seriya-4-v-forza-horizon-6-luchshie-mashiny-i-tyuning) доступен. Новых подтверждённых исправлений не установлено. |
| DungG Seasonal Playlist | Прямой YouTube-плейлист недоступен, адресный поиск DungG/Series 4/Winter не дал подтверждённого выпуска. Старые видео не использованы. |

## Ежедневное уточнение — 2026-09-02 06:04 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Сохраняются 14 карточек, один Daily из семи дней и максимум 53 очка; rollover не выполнялся.
- Сводка актуальна — содержательных изменений не требуется. После проверки всех обязательных источников не найдено новых подтверждённых исправлений условий, решений, машин, 9-значных share codes или `openItems`. Для Matsumi Curve сохранена безопасная цель 75 mph: её подтверждают точная игровая плитка ForzaLabs, Fandom Winter и свежие недельные материалы, тогда как официальная веб-таблица всё ещё показывает ошибочные 70 mph.
- Отдельно перепроверены все 14 `visual`: все локальные файлы существуют и имеют 14 разных SHA-256. Итог: `confirmed: 13`, `community: 0`, `preliminary: 1`, `missing: 0`. Единственный открытый пункт — отдельная точная плитка объединённого Daily: Fandom Winter revision `170723` по-прежнему содержит 53 изображения без Daily-плитки, ForzaLabs Series Details не публикует отдельный Daily-блок, а свежий поиск изображений не дал точного кадра текущей недели.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: в категории остаются Series 1–4 и пустая Category:Series 5; смена активной Series не подтверждена. |
| Forza Wiki / Fandom | Точная Winter Season остаётся на revision `170723` от 29 августа; условия и 53 изображения не изменились, отдельной Daily-плитки нет. |
| Official Forza Festival Playlist | Живой HTML, проиндексированный сегодня, подтверждает S04 Winter 27.08–03.09, семь Daily, порядок 14 карточек, ограничения и награды; новой поправки к неделе нет. |
| Official Forza News | Проверены Series 4 News и последняя FH6-новость `Shift Into High Gear with Drift Attack!` от 26 августа; она анонсирует сентябрьский режим и не меняет активную Winter Playlist. |
| Forza Support Release Notes | Секция снова отвечает внутренней ошибкой, но связанный список статей подтверждает последним `FH6 Release Notes: August 24, 2026`; более свежего индексируемого патча, меняющего Winter Playlist, нет. |
| Forza Support Known Issues | Страница доступна и сегодня проверена; она по-прежнему датирована 20 июля и не содержит отдельной проблемы текущей Winter Playlist. |
| Official Forza Forums | Старый official-info URL перенаправляет на страницу закрытых форумов; свежего официального Winter-треда или поправки нет. |
| Reddit r/ForzaHorizon | Проверены текущие Winter breakdown и tuning guide, включая комментарии; подтверждённых исправлений после предыдущего аудита и отдельной Daily-плитки нет. |
| Reddit r/ForzaHorizon6 | Полный Winter guide и свежие tuning posts остаются актуальными; новых решений, ошибок условий или более точного Daily-визуала не опубликовано. |
| Reddit r/forza | Winter Information Thread и tuning guide подтверждают дедлайн, 53 очка и безопасную цель Matsumi Curve 75 mph; новых поправок нет. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Winter-поста в доступном поисковом индексе не найдено; старые настройки не переносились. |
| Forza Horizon Hub | Сайт доступен и показывает 632 машины, но недельный блок всё ещё заявляет Series 1; текущие Winter-факты и visual оттуда не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог из 628 машин; отдельного нового текущенедельного решения, кода или Daily-изображения нет. |
| ForzaLabs Interactive Map | Карта доступна; нового Winter-маркера, превосходящего уже опубликованные карту и скриншот Ohtani, не найдено. |
| ForzaLabs Series Details | Живая страница подтверждает Horizon Mascot Party Winter и 13 точных activity-визуалов; отдельного Daily-блока или изображения нет. |
| Escorenews FH6 | Winter guide, Trial и Ohtani Treasure Hunt от 27 августа остаются последними; более свежей содержательной поправки нет. |
| DungG Seasonal Playlist | Прямой плейлист недоступен для чтения, а индексируемого выпуска DungG по Series 4 Winter не найдено; данные прошлых недель не использовались. |

## Ежедневное уточнение — 2026-09-01 06:04 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Сохраняются 14 карточек, один Daily из семи дней и максимум 53 очка; rollover не выполнялся.
- Сводка актуальна — содержательных изменений не требуется. Новых подтверждённых исправлений условий, решений, машин, 9-значных share codes или `openItems` после проверки всех обязательных источников не найдено.
- Отдельно перепроверены все 14 visual: локальные файлы существуют и имеют 14 разных SHA-256. Итог: `confirmed: 13`, `community: 0`, `preliminary: 1`, `missing: 0`. Единственный открытый пункт — отдельная точная плитка объединённого Daily; Fandom Winter revision `170723` по-прежнему содержит 53 изображения без Daily-плитки, а ForzaLabs Series Details не публикует отдельное Daily-изображение.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: в категории остаются Series 1–4 и пустая Category:Series 5; смена активной Series не подтверждена. |
| Forza Wiki / Fandom | Точная Winter Season остаётся на revision `170723`; условия и 53 изображения не изменились, отдельной Daily-плитки нет. |
| Official Forza Festival Playlist | Живой HTML сегодня подтверждает S04 Winter, семь Daily, порядок 14 карточек, ограничения и награды; новой поправки к неделе нет. |
| Official Forza News | Раздел проверен; более свежей новости, меняющей Horizon Mascot Party Winter или её Playlist, не опубликовано. |
| Forza Support Release Notes | Прямая секция снова недоступна; свежего индексируемого патча после Series 4 Hotfix 1 от 24 августа, меняющего Winter Playlist, не найдено. |
| Forza Support Known Issues | Страница доступна и сегодня проверена; отдельной проблемы текущей Winter Playlist в списке нет. |
| Official Forza Forums | URL перенаправляет на общую страницу Forza Forums; свежего официального Winter-треда или поправки нет. |
| Reddit r/ForzaHorizon | Проверены Winter breakdown и свежие текущенедельные tune-публикации; подтверждённых исправлений после предыдущего аудита и отдельной Daily-плитки нет. |
| Reddit r/ForzaHorizon6 | Полный Winter guide и текущенедельные tuning posts остаются актуальными; новых решений или исправлений карточек не опубликовано. |
| Reddit r/forza | Winter Information Thread и свежие tune-подборки проверены; дедлайн, 53 очка и условия не изменились. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Winter-поста в доступном поисковом индексе не найдено; старые настройки не переносились. |
| Forza Horizon Hub | Сайт доступен, но текущего Series 4 Winter weekly-блока не показывает; факты и visual оттуда не брались. |
| ForzaLabs Collector Tool | Каталог доступен; отдельного нового текущенедельного решения, кода или Daily-изображения нет. |
| ForzaLabs Interactive Map | Карта проверена; нового Winter-маркера, превосходящего уже опубликованные карту и скриншот Ohtani, нет. |
| ForzaLabs Series Details | Живая страница по-прежнему подтверждает текущую Winter и 13 точных activity-визуалов; отдельного Daily-блока или изображения нет. |
| Escorenews FH6 | Актуальные Winter-гайды от 27 августа остаются последними; новых поправок к решениям и маршрутам не найдено. |
| DungG Seasonal Playlist | Плейлист проверен; индексируемого выпуска Series 4 Winter по-прежнему нет, данные прошлых недель не использовались. |

## Внеплановое ежедневное уточнение — 2026-08-31 07:18 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Сохраняются 14 карточек, один Daily из семи дней и максимум 53 очка; rollover не выполнялся.
- Закрыт конфликт `Matsumi Curve`: точная игровая карточка текущей недели в ForzaLabs показывает `75.0 mph`, а актуальная Fandom-страница Winter revision `170723` независимо содержит ту же цель `75.0 mph`. Официальная веб-таблица Forza всё ещё показывает 70 mph, поэтому она явно отмечена как ошибочная веб-запись, а публичное условие теперь подтверждено по фактической игровой карточке.
- Визуал Matsumi Curve заменён на точный игровой экран с целью 75 mph и ограничением Eclectic Domestics D400; файл приведён к 720×720. Аудит всех карточек: `confirmed: 13`, `community: 0`, `preliminary: 1`, `missing: 0`. Только объединённый Daily остаётся временным визуалом: среди 53 файлов текущей Fandom Winter отдельной Daily-плитки нет.
- Свежие текущенедельные tune-подборки от 29 августа проверены. Они дают дополнительные варианты, но не доказывают ошибку или превосходство над уже опубликованными свежими кодами, поэтому рекомендации машин и share codes не менялись. После уточнения Matsumi Curve остаётся `openItems: 1`.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: в категории есть Series 1–4 и пустая категория Series 5; смена активной Series не подтверждена. |
| Forza Wiki / Fandom | Точная страница `Forza Horizon 6/Series 4/Winter Season` доступна, revision `170723`; в wikitext Matsumi Curve указан как 75.0 mph. Из 53 файлов отдельной Daily-плитки нет. |
| Official Forza Festival Playlist | Живой HTML подтверждает S04 Winter, все семь Daily, 14 карточек, ограничения и награды; веб-строка Matsumi Curve по-прежнему ошибочно показывает 70 mph. |
| Official Forza News | `Join the Horizon Mascot Party` подтверждает Winter 27.08–03.09 и награды 20/40 очков; более свежая новость Drift Attack не меняет текущую Playlist. |
| Forza Support Release Notes | Прямая секция/API в этом запуске недоступна; свежего индексируемого патча после Series 4 Hotfix 1 от 24 августа, меняющего Winter Playlist, не найдено. |
| Forza Support Known Issues | Страница доступна; отдельной официальной проблемы Winter Playlist или Matsumi Curve в списке нет. |
| Official Forza Forums | URL перенаправляет на общую страницу Forza Forums; свежего официального Winter-треда или поправки к неделе нет. |
| Reddit r/ForzaHorizon | Проверены текущий Winter breakdown и свежая tuning guide от 29 августа; breakdown подтверждает безопасную цель 75 mph. |
| Reddit r/ForzaHorizon6 | Проверены полный Winter guide и свежая tuning guide; новых ошибок карточек или отдельной Daily-плитки не опубликовано. |
| Reddit r/forza | Winter Information Thread подтверждает дедлайн, 53 очка и Matsumi Curve 75 mph; свежая tuning guide проверена как набор альтернатив. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Winter-поста в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен и показывает 632 машины, но недельный блок остаётся на Series 1; текущие Winter-факты оттуда не брались. |
| ForzaLabs Collector Tool | HTTP 200; общий каталог доступен, отдельного текущенедельного решения или тюнинга нет. |
| ForzaLabs Interactive Map | HTTP 200; карта доступна, нового Winter-маркера Ohtani точнее опубликованного скриншота нет. |
| ForzaLabs Series Details | Живая страница подтверждает Winter и содержит точный detail-экран Matsumi Curve: 75 mph, D400 Eclectic Domestics, Wheelspin. |
| Escorenews FH6 | Проверены актуальные Winter-гайды от 27 августа; сундук, Trial и маршруты остаются актуальными, веб-гайд повторяет устаревшие 70 mph. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200, но индексируемого выпуска Series 4 Winter не найдено; данные прошлых недель не переносились. |

## Ежедневное уточнение — 2026-08-30 06:07 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Структура не изменилась: 14 карточек, один Daily с семью днями и максимум 53 очка; rollover не выполнялся.
- ForzaLabs Series Details теперь показывает точные игровые плитки текущей Winter. Двенадцать прежних community-визуалов заменены компактными локальными квадратами 720×720; Mini Games уже использовал точную плитку. Итог проверки всех карточек: `confirmed: 13`, `community: 0`, `preliminary: 1`, `missing: 0`. Только объединённый Daily остаётся временным визуалом и открытым пунктом.
- Новые текущенедельные tune-подборки сверены с опубликованными рекомендациями. Они дают дополнительные варианты для Micro Circuits и Modern Marvels, но не устраняют существующие неопределённости и не подтверждают превосходство над уже опубликованными кодами, поэтому коды карточек не менялись.
- Конфликт Matsumi Curve остаётся открытым: официальная Playlist указывает 70 mph, Winter Information Thread — 75 mph, а свежая competitive-подборка снова приводит 70 mph. В карточке сохранена безопасная цель 75 mph.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Категория проверена: Series 4 остаётся текущей; подтверждения Series 5 или нового активного сезона нет. |
| Forza Wiki / Fandom | Точная страница `Forza Horizon 6/Series 4/Winter Season` всё ещё недоступна/не индексируется; нового отдельного Daily-визуала нет. |
| Official Forza Festival Playlist | Живой HTML подтверждает S04 Winter, 14 карточек, семь Daily, все ограничения и награды; официальный Matsumi Curve остаётся 70 mph. |
| Official Forza News | `Join the Horizon Mascot Party` подтверждает Winter 27.08–03.09; свежие Drift Attack и Toyota Celica не меняют условия Playlist. |
| Forza Support Release Notes | Прямая страница недоступна; последним подтверждённым остаётся Series 4 Hotfix 1 от 24 августа без изменений Winter Playlist. |
| Forza Support Known Issues | Страница доступна; нового пункта о Winter-карточках или Matsumi Curve не опубликовано. |
| Official Forza Forums | Свежего официального Winter-треда или поправки к активной неделе нет. |
| Reddit r/ForzaHorizon | Актуальный Winter breakdown проверен; новых подтверждённых исправлений условий или отдельного Daily-визуала нет. |
| Reddit r/ForzaHorizon6 | Полный Winter guide и свежая competitive tune-подборка проверены; условия и опубликованные решения остаются актуальными. |
| Reddit r/forza | Winter Information Thread подтверждает 53 очка, дедлайн и порядок; свежая tune-подборка сверена без замены уже опубликованных кодов. |
| Reddit r/ForzaTune | Отдельного свежего материала FH6 Series 4 Winter не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен, но недельный блок остаётся на Series 1; текущие факты и коды оттуда не брались. |
| ForzaLabs Collector Tool | Инструмент доступен; общий каталог содержит 628 машин, но отдельного текущенедельного решения или тюнинга нет. |
| ForzaLabs Interactive Map | Карта доступна; отдельного Winter-маркера Ohtani, превосходящего опубликованный ориентир, не найдено. |
| ForzaLabs Series Details | Живая страница подтверждает Series 4 Winter и предоставляет точные игровые плитки для 13 карточек; они сохранены локально. |
| Escorenews FH6 | Прямой раздел вернул внутреннюю ошибку; индексируемые Winter-гайды от 27 августа остаются последними, новых поправок не найдено. |
| DungG Seasonal Playlist | Прямое чтение ограничено, индексируемого выпуска Series 4 Winter не найдено; прошлосезонные данные не использовались. |

## Ежедневное уточнение — 2026-08-29 06:01 +07:00

- Живая официальная Playlist и Series 4 News подтверждают прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Фактическая структура не изменилась: 14 карточек, один Daily с семью днями и максимум 53 очка; rollover не выполнялся.
- В новых текущенедельных обсуждениях найден более устойчивый вариант для `Micro Circuits`: 1991 Honda Beat A700, код `120 569 217`. Honda Beat отдельно подтверждён как допустимый Microcar Madness. Для `Edamame Time Attack` добавлен 1971 Nissan Skyline 2000GT-R C500, код `560 632 810`, с описанной автором предсказуемой управляемостью. Оба совета сообщества в проекте помечены как не подтверждённые в игре.
- ForzaLabs опубликовал точную игровую плитку Winter `Mini Games`: она скачана локально, приведена к квадрату 720×720 и заменила временный reward-визуал. Независимо проверены все 14 файлов: все существуют, квадратные и имеют разные SHA-256. Итог: `confirmed: 1`, `community: 12`, `preliminary: 1`, `missing: 0`; открыты только отдельный Daily-визуал и конфликт порога Matsumi Curve (`openItems: 2`).
- Конфликт Matsumi Curve не закрыт: официальная Playlist по-прежнему показывает 70 mph, два свежих Reddit-гайда — 75 mph. Публичная карточка сохраняет оба значения и безопасную цель 75 mph.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API проверен: Series 4 остаётся текущей; Category:Series 5 не содержит подтверждения новой Series или смены активного сезона. |
| Forza Wiki / Fandom | Точная страница `Forza Horizon 6/Series 4/Winter Season` через API всё ещё возвращает `missing`; нового отдельного Daily-визуала нет. |
| Official Forza Festival Playlist | Живой HTML подтверждает S04 Winter, 14 карточек, семь Daily, все ограничения и награды; официальный Matsumi Curve остаётся 70 mph. |
| Official Forza News | `Join the Horizon Mascot Party` подтверждает Winter 27.08–03.09 и награды 20/40 очков; свежая новость про Toyota Celica не меняет условия Playlist. |
| Forza Support Release Notes | Последним остаётся Series 4 Hotfix 1 от 24 августа; исправления Road Discovery и Creative Hub не затрагивают Winter Playlist. |
| Forza Support Known Issues | Нового официального пункта о Winter-карточках или Matsumi Curve не опубликовано; прямой Help Center остаётся ограничен, проверен доступный индекс. |
| Official Forza Forums | Свежего официального Winter-треда нет; архивный форум не содержит поправки к активной неделе. |
| Reddit r/ForzaHorizon | Свежие Winter breakdown и дубли текущенедельных tune-подборок проверены; новых официально подтверждённых исправлений условий нет. |
| Reddit r/ForzaHorizon6 | Проверены полный Winter guide, новые комментарии, подборка Awes0me Beau и список Microcar Madness; на их основе заменены две рекомендации и коды. |
| Reddit r/forza | Winter Information Thread подтверждает 53 очка, дедлайн и порядок; свежие альтернативные тюнинги сверены без переноса старых кодов. |
| Reddit r/ForzaTune | Отдельного свежего материала FH6 Series 4 Winter в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен, но недельный блок всё ещё показывает Series 1; текущие Winter-факты и коды оттуда не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и содержит общий каталог 628 машин, но не даёт отдельного текущенедельного решения или тюнинга. |
| ForzaLabs Interactive Map | Карта доступна с категориями Photography, Treasure, PR Stunts и трасс; отдельного Winter-маркера Ohtani, превосходящего текущий прямой скриншот, нет. |
| Escorenews FH6 | Свежие Winter-гайды AutoZOOM, Treasure, Trial и полный сезонный разбор остаются актуальными; новых поправок после 27 августа не найдено. |
| DungG Seasonal Playlist | Прямое чтение YouTube ограничено, а индексируемого выпуска Series 4 Winter/Horizon Mascot Party не найдено; прошлосезонное видео не использовалось. |

## Ежедневное уточнение — 2026-08-28 06:07 +07:00

- Живая официальная Playlist, официальная статья Series 4 и свежий Winter Information Thread подтверждают прежний активный сезон `Series 4 — Horizon Mascot Party / Winter` до 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Порядок 14 карточек, семь Daily, ограничения, награды и максимум 53 очка не изменились; rollover не выполнялся.
- После вечернего rollover появился полноценный текущенедельный гайд Escorenews и отдельные материалы Treasure/Trial. Добавлены более точные ориентиры: Treasure находится на грунтовой дороге под Matsumi Great Bridge в южной части Ohtani; Shirakawa-go удобнее брать с северо-запада, Highland Road — с северо-востока, Matsumi Curve — с левого входа. Для Trial добавлены предупреждения о 90-градусных поворотах и скрытом деревьями узком мосте. Машины и share codes не менялись: уже опубликованный набор остаётся свежим для этой недели, а новые альтернативы не получили сравнительного игрового подтверждения.
- Конфликт Matsumi Curve остаётся открытым: официальный HTML и новый Escorenews-гайд указывают 70 mph, а два свежих Reddit-гайда — 75 mph. Публичная карточка по-прежнему показывает оба значения и рекомендует целиться в 75 mph для надёжного зачёта.
- Отдельно проверены все 14 `visual`: точная Fandom Winter Season всё ещё отсутствует, новых отдельных плиток Daily и Mini Games в свежих материалах не найдено. Все 14 локальных файлов существуют, имеют разные SHA-256 и относятся к текущей Winter-неделе. Итог: `confirmed: 0`, `community: 12`, `preliminary: 2`, `missing: 0`; открыты только замены Daily/Mini Games и конфликт Matsumi Curve (`openItems: 3`).

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: Series 4 остаётся текущей; Category:Series 5 по-прежнему не содержит страницы новой Series и не меняет активный сезон. |
| Forza Wiki / Fandom | API для `Forza Horizon 6/Series 4/Winter Season` всё ещё возвращает `missing`; точных Winter-плиток для Daily и Mini Games не появилось. |
| Official Forza Festival Playlist | Живой HTML подтверждает строки S04 Winter: 14 карточек, семь Daily, условия, трассы, ограничения и награды. Для Matsumi Curve официальный порог остаётся 70 mph. |
| Official Forza News | Статья `Join the Horizon Mascot Party` подтверждает Winter 27.08–03.09 и сезонные награды; более свежей поправки к карточкам не опубликовано. |
| Forza Support Release Notes | Прямой Help Center вернул 403, но поиск и Steam Events подтверждают последнюю публикацию `Series 4 Hotfix 1` от 24 августа; её исправления Road Discovery и Creative Hub не затрагивают Winter Playlist. |
| Forza Support Known Issues | Прямая страница вернула 403; поисковый индекс не показывает нового официального пункта про Winter-карточки или конфликт Matsumi Curve. |
| Official Forza Forums | URL доступен, но свежего официального Winter-треда после закрытия форума нет; актуальные данные остаются на Forza.net. |
| Reddit r/ForzaHorizon | Свежий Winter breakdown и комментарии проверены; подтверждены 53 очка, условия недели и игровой порог Matsumi Curve 75 mph. Новых отдельных Daily/Mini Games плиток нет. |
| Reddit r/ForzaHorizon6 | Полный Winter guide и свежие комментарии проверены; существующие решения, изображения и основной набор кодов остаются актуальными. Исправленное название Trial уже учтено в проекте. |
| Reddit r/forza | Winter Information Thread подтверждает дедлайн, 53 очка и фактический порядок; появились альтернативные свежие tune-наборы, но без доказанного преимущества над опубликованными кодами. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Winter поста в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | HTTP 200, но главная по-прежнему содержит Series 1 и не содержит Series 4/Winter; текущие факты и визуалы оттуда не брались. |
| ForzaLabs Collector Tool | HTTP 200; в данных встречаются Series 4 и Ohtani, но отдельного текущенедельного Winter-решения или набора плиток нет. |
| ForzaLabs Interactive Map | HTTP 200; отдельного маркера Ohtani/Winter, превосходящего свежий прямой скриншот и гайд Matsumi Great Bridge, не найдено. |
| Escorenews FH6 | Найдены свежие материалы от 27 августа: полный Winter-гайд, отдельный Treasure Hunt и подробный Trial. Практические направления и ссылки добавлены в пять карточек. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200, но в его доступном HTML и поисковом индексе нет выпуска Series 4 Winter/Horizon Mascot Party; прошлосезонное видео не использовалось. |

## Внеплановый rollover — 2026-08-27 21:46 +07:00

- Живая официальная Festival Playlist после сброса подтвердила новый активный сезон `Series 4 — Horizon Mascot Party / Winter`: 27 августа — 3 сентября 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Фактическая структура: 14 карточек, один блок Daily с 7 днями, максимум 53 очка. Арифметика: `5 + 7 + 2 + 3 + 5 + 5 + 3 + 2 + 2 + 2 + 10 + 3 + 3 + 1 = 53`.
- В свежем текущенедельном гайде r/ForzaHorizon6 найдены прямой скриншот сундука Ohtani, практические решения и новые девятизначные share codes: `828 279 003`, `124 380 195`, `599 539 660`, `143 289 036`, `860 360 277`, `665 682 998`. Коды прошлой недели не переносились; советы сообщества в игре не подтверждены.
- Найдено 12 отдельных текущенедельных activity/reward-скриншотов из свежей Winter-галереи Reddit. Для объединённого Daily и Mini Games отдельных плиток пока нет: использованы два разных текущесезонных reward-визуала со статусом `preliminary`. Все 14 локальных изображений имеют размер 720×720 и разные SHA-256. Итог visual: `confirmed: 0`, `community: 12`, `preliminary: 2`, `missing: 0`.
- Открыт конфликт для Speed Zone `Matsumi Curve`: официальная таблица указывает 70 mph (112,7 км/ч), тогда как два свежих текущенедельных гайда показывают 75 mph (120,7 км/ч). В публичной карточке сохранены оба значения и безопасная рекомендация целиться в 75 mph до появления точного скриншота игровой цели.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: Series 4 остаётся текущей, а пустая Category:Series 5 не подтверждает новую Series. |
| Forza Wiki / Fandom | Точная страница `Forza Horizon 6/Series 4/Winter Season` через API пока возвращает `missing`; точные Winter-плитки с Fandom ещё не опубликованы. |
| Official Forza Festival Playlist | Живой HTML после 21:30 +07 содержит все строки S04 Winter: 14 карточек, семь Daily, ограничения, трассы, награды и 53 очка. Это основной источник rollover. |
| Official Forza News | Статья `Join the Horizon Mascot Party` подтверждает Winter 27.08–03.09 и награды 1974 Toyota Celica GT / 1989 Toyota MR2 SC; статья Drift Attack от 26 августа текущие карточки не меняет. |
| Forza Support Release Notes | Последними остаются `FH6 Release Notes: August 24, 2026` (Series 4 Hotfix 1); изменений условий Winter Playlist в них нет. |
| Forza Support Known Issues | Страница доступна и датирована 20 июля; отдельной официальной записи о новых Winter-испытаниях или конфликте Matsumi Curve нет. |
| Official Forza Forums | URL official-info перенаправляет на страницу о закрытии форума; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Найдены свежие Winter breakdown, список допустимых Microcar Madness и второе подтверждение игровой цели Matsumi Curve 75 mph. |
| Reddit r/ForzaHorizon6 | Найден полный Winter guide, опубликованный после сброса: решения, прямой скриншот Treasure, текущенедельные коды и отдельные изображения карточек/наград. |
| Reddit r/forza | Найден свежий Winter tuning guide с альтернативными текущенедельными кодами; основной набор не заменён без игрового сравнения. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Winter материала в поисковом индексе не найдено; старые настройки не использовались. |
| Forza Horizon Hub | Сайт доступен, но его недельный блок всё ещё показывает Series 1 и дату проверки 27 мая; Winter-факты из него не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает общий автомобильный реестр; отдельного текущенедельного Winter-решения или плиток нет. |
| ForzaLabs Interactive Map | Карта доступна с общими категориями markers, photography и treasure; отдельного подтверждённого Winter-маркера Ohtani не найдено. |
| Escorenews FH6 | Раздел и поиск проверены; свежего материала Series 4 Winter на момент запуска нет, найденный Winter-гайд относится к Series 2. |
| DungG Seasonal Playlist | Плейлист проверен; прямое чтение YouTube ограничено, а индексируемого выпуска Series 4 Winter на момент запуска нет. Прошлосезонные видео не использовались. |

## Ежедневное уточнение — 2026-08-27 06:04 +07:00

- Живая официальная Playlist по-прежнему подтверждает активный `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). На момент проверки до сброса оставалось более 15 часов: опубликованные ниже строки Winter являются предварительным архивом следующей недели, а не подтверждением уже состоявшегося rollover. Порядок 14 карточек, семь Daily, ограничения, награды и максимум 52 очка Autumn не изменились.
- Проверены `openItems`, `missingFields`, пустые поля, TODO и конфликты: `openItems: 0`, `missingFields: 0`, пустых обязательных полей нет. Новый официальный материал `Shift Into High Gear with Drift Attack!` от 26 августа посвящён будущему режиму Drift Attack и не меняет текущую Playlist. Новый общественный каталог тюнингов от 24 августа не подтверждает ошибку или преимущество перед уже опубликованными текущенедельными кодами, поэтому карточки не менялись.
- Отдельно перепроверены все 14 `visual`: Fandom Autumn остаётся на revision `170211`, список десяти точных сезонных изображений не изменился; новых отдельных плиток для Weekly, общего Daily, Hide & Seek и Stunt Party не появилось. Все локальные изображения доступны, квадратные 720×720 и имеют разные SHA-256. Итог: `confirmed: 10`, `community: 4`, `preliminary: 0`, `missing: 0`.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: Series 4 остаётся текущей; в категории по-прежнему есть только пустая Category:Series 5 без страницы новой Series и без подтверждения смены сезона. |
| Forza Wiki / Fandom | Точная Autumn Season доступна на revision 170211 от 25 августа. Галерея по-прежнему содержит десять отдельных текущенедельных изображений; новых точных плиток для оставшихся четырёх карточек нет. |
| Official Forza Festival Playlist | Живой HTML, обновлённый в индексе сегодня, подтверждает `Horizon Mascot Party — Autumn` 20–27 августа и все 14 текущих активностей без поправок. Заранее опубликованные строки Winter не активны до сброса 14:30 UTC. |
| Official Forza News | Проверены Series 4 News и новая статья `Shift Into High Gear with Drift Attack!` от 26 августа; новая статья анонсирует будущий режим и не меняет Autumn Festival Playlist. |
| Forza Support Release Notes | Последними остаются `FH6 Release Notes: August 24, 2026`, Series 4 Hotfix 1; исправления Road Discovery Progress и прав на винилы не затрагивают карточки недели. |
| Forza Support Known Issues | Статья доступна, обновлена 20 июля и перенаправляет к Feedback Portal; отдельного официального пункта о текущих Autumn-испытаниях нет. |
| Official Forza Forums | URL official-info снова перенаправляет на страницу закрытых форумов; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Текущенедельные Autumn tuning guide и breakdown остаются актуальными; свежих подтверждённых исправлений условий, решений или кодов после прошлого аудита не найдено. |
| Reddit r/ForzaHorizon6 | Полный Autumn Festival Playlist guide, tuning guide и доступные комментарии проверены; новых поправок Photo/Collectibles, Trial, PR Stunts или визуалов нет. |
| Reddit r/forza | Autumn tuning guide и новый общий Tune Database от 24 августа проверены; каталог не даёт текущенедельного доказательства, требующего заменить опубликованные рекомендации. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Autumn материала в поисковом индексе не найдено; старые настройки не переносились. |
| Forza Horizon Hub | Сайт доступен, но его недельный блок всё ещё показывает Series 1 и данные, проверенные 27 мая; текущие Autumn-факты из него не брались. |
| ForzaLabs Collector Tool | Инструмент доступен; отдельного текущенедельного материала по Homerun или новых карточных изображений нет. |
| ForzaLabs Interactive Map | Карта доступна и индексируется как общий реестр маркеров; отдельного подтверждённого Autumn-маркера, меняющего опубликованные решения, нет. |
| Escorenews FH6 | Autumn guide, Weekly, Photo и Collectibles материалы от 20 августа доступны и сегодня повторно проиндексированы; более свежей содержательной поправки нет. |
| DungG Seasonal Playlist | Прямое открытие по-прежнему уводит на YouTube consent, а индексируемого выпуска DungG по Series 4 Autumn не найдено; прошлосезонные видео не использовались. |

## Ежедневное уточнение — 2026-08-26 06:09 +07:00

- Живая официальная Playlist по-прежнему подтверждает активный `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Порядок 14 карточек, семь Daily, ограничения, награды и максимум 52 очка не изменились; rollover не выполнялся.
- Fandom 25 августа создал точную страницу `Forza Horizon 6/Series 4/Autumn Season`, revision `170211`. Из её галереи скачаны, визуально сопоставлены с активностями, обрезаны в квадрат 720×720 и оптимизированы десять отдельных текущенедельных изображений: Photo, Collectibles, оба чемпионата, две Speed Zone, Trailblazer, Trial, Squeaky Clean и Monthly Rivals. Имена `Champ1`/`Champ2` в галерее не соответствуют изображённым дисциплинам, поэтому файлы сопоставлены по фактическому содержимому кадра.
- Итог независимого аудита всех 14 `visual`: `confirmed: 10`, `community: 4`, `preliminary: 0`, `missing: 0`; все 14 локальных файлов квадратные и имеют разные SHA-256. Для Weekly, общего Daily, Hide & Seek и Stunt Party точных отдельных Fandom-плиток пока нет, поэтому сохранены разные актуальные community-визуалы текущей недели.
- Проверены `openItems`, `missingFields`, пустые поля, TODO, новые комментарии и конфликты: `openItems: 0`, `missingFields: 0`. Новых подтверждённых исправлений прохождения или преимуществ у альтернативных текущенедельных share codes не найдено; фактический текст карточек не менялся.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: Series 4 остаётся текущей; в категории есть только заготовка Series 5 без страницы Series и без подтверждения смены сезона. |
| Forza Wiki / Fandom | Новая Autumn Season revision 170211 от 25 августа содержит галерею с десятью отдельными текущенедельными визуалами; они заменили community-версии. Ошибочные подписи/поля страницы не использовались вместо официальной Playlist. |
| Official Forza Festival Playlist | Живой HTML подтверждает `Horizon Mascot Party — Autumn` 20–27 августа, все 14 активностей, текущие условия, трассы, ограничения и награды без поправок. |
| Official Forza News | Раздел News и статья `Join the Horizon Mascot Party` проверены; новая публикация от 25 августа посвящена распродаже и не меняет текущую Playlist. |
| Forza Support Release Notes | Последними остаются `FH6 Release Notes: August 24, 2026`, Series 4 Hotfix 1; исправления Road Discovery Progress и винилов не затрагивают карточки недели. |
| Forza Support Known Issues | Статья доступна и по-прежнему датирована 20 июля; отдельного официального пункта о текущих Autumn-испытаниях нет. |
| Official Forza Forums | URL official-info снова перенаправляет на страницу о закрытии форумов; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Текущенедельные Autumn breakdown и tuning guide вместе с доступными комментариями проверены; новой подтверждённой поправки после прошлого аудита нет. |
| Reddit r/ForzaHorizon6 | Полный Autumn Festival Playlist guide, отдельный tuning guide и доступные комментарии остаются актуальными; новых исправлений условий, решения Photo/Collectibles или кодов нет. |
| Reddit r/forza | `Autumn Information Thread — Series 4` и текущенедельный tuning guide по-прежнему подтверждают дедлайн, 52 очка и опубликованный порядок; новых поправок нет. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Autumn материала в поисковом индексе не найдено; старые настройки не переносились. |
| Forza Horizon Hub | Сайт доступен, но его недельный блок всё ещё показывает Series 1; текущие Autumn-факты и изображения из него не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает 628 автомобилей; отдельного текущенедельного материала по Homerun или карточных изображений нет. |
| ForzaLabs Interactive Map | Карта доступна с категориями mascots, photography и PR Stunts; отдельного подтверждённого Autumn-маркера, меняющего опубликованные решения, нет. |
| Escorenews FH6 | Autumn guide, Weekly, Photo и Collectibles материалы от 20 августа доступны и подтверждают текущие решения; более свежей содержательной поправки не опубликовано. |
| DungG Seasonal Playlist | Прямое чтение YouTube-плейлиста ограничено throttling, а индексируемого выпуска DungG по Series 4 Autumn не найдено; прошлосезонные видео не использовались. |

## Ежедневное уточнение — 2026-08-25 06:05 +07:00

- Живая официальная Playlist и официальная статья Series 4 подтверждают прежний активный `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Порядок 14 карточек, семь Daily, ограничения, награды и максимум 52 очка не изменились; rollover не выполнялся.
- Forza Support опубликовала `FH6 Release Notes: August 24, 2026` (Series 4 Hotfix 1). Исправлены потеря Road Discovery Progress и возможность скачивать/редактировать чужие винилы; изменений условий, подсчёта очков, Photo/Collectibles, Trial, PR Stunts или share codes текущей недели в хотфиксе нет, поэтому карточки не менялись.
- Проверены `openItems`, `missingFields`, пустые поля, TODO и конфликты: `openItems: 0`, `missingFields: 0`, новых подтверждённых ошибок прохождения или преимуществ у альтернативных текущенедельных кодов не найдено.
- Отдельно проверены все 14 `visual`: локальные файлы присутствуют, имеют 14 разных SHA-256 и относятся к текущей Autumn-неделе. Итог полноты: `confirmed: 0`, `community: 14`, `preliminary: 0`, `missing: 0`. Fandom всё ещё не создал точную Autumn Season страницу, а официальные источники и свежие гайды не дали более точного полного набора игровых плиток.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Прямой URL ограничен robots/403, MediaWiki API доступен: Series 4 остаётся текущей; есть только пустая категория Series 5, без подтверждения смены сезона. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169617 от 17 августа; API для `Forza Horizon 6/Series 4/Autumn Season` возвращает `missing`, точных Autumn-плиток не опубликовано. |
| Official Forza Festival Playlist | Живой HTML подтверждает `Horizon Mascot Party — Autumn` 20–27 августа, все текущие названия, порядок, условия, трассы и награды без поправок. |
| Official Forza News | Статья `Join the Horizon Mascot Party` от 10 августа подтверждает Autumn 20–27 августа и сезонные награды; новой официальной поправки к Playlist нет. |
| Forza Support Release Notes | Найден новый `Series 4 Hotfix 1` от 24 августа: исправлены Road Discovery Progress и права на винилы; текущие карточки Festival Playlist не изменены. |
| Forza Support Known Issues | Статья доступна и по-прежнему датирована 20 июля; отдельного официального пункта о текущих Autumn-испытаниях нет. |
| Official Forza Forums | Старый official-info URL перенаправляет на страницу о закрытии форума; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Проверены текущенедельные Autumn breakdown и tuning guide от 20–21 августа; новые комментарии не подтверждают ошибку опубликованных решений или кодов. |
| Reddit r/ForzaHorizon6 | Полный Autumn guide, отдельный tuning guide и свежие комментарии проверены; новых исправлений условий или более точного полного набора визуалов нет. |
| Reddit r/forza | `Autumn Information Thread — Series 4` и текущенедельный tuning guide подтверждают дедлайн, 52 очка и опубликованные активности; новых поправок нет. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Autumn материала в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен, но его блок Festival Playlist всё ещё показывает Series 1; актуальной Autumn-публикации, решения или плиток нет. |
| ForzaLabs Collector Tool | Инструмент доступен и обновляет автомобильный реестр, но отдельного текущенедельного материала по Shimanoyama Heat не публикует. |
| ForzaLabs Interactive Map | Карта доступна с категориями mascots/photography/PR Stunts, но отдельного подтверждённого Autumn-маркера или более точного решения не найдено. |
| Escorenews FH6 | Актуальные Autumn guide, Weekly, Photo и Collectibles материалы от 20 августа доступны и по-прежнему подтверждают опубликованные решения; свежей поправки нет. |
| DungG Seasonal Playlist | Прямое чтение YouTube было ограничено throttling, а индексируемого выпуска DungG по Series 4 Autumn не найдено; прошлосезонные видео не использовались. |

## Ежедневное уточнение — 2026-08-24 06:01 +07:00

- Живая официальная Playlist и официальная статья Series 4 подтверждают прежний активный `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Порядок 14 карточек, семь Daily, ограничения, награды и максимум 52 очка не изменились; rollover не выполнялся.
- Уточнено выполнение `#DeliciousDango`: свежая версия текущенедельного Escorenews-гайда явно отделяет нужные картонные фигуры трёх данго от розовых щитов Tokyo City — снимок только у щитов может не засчитаться. Карточка теперь ведёт к фигурам на центральной парковке; новый код или автомобиль для испытания не требуется.
- Проверены все 14 `visual`: локальные файлы присутствуют, имеют 14 разных SHA-256 и относятся к текущей Autumn-неделе. Итог полноты: `confirmed: 0`, `community: 14`, `preliminary: 0`, `missing: 0`; точная Fandom-страница Autumn всё ещё отсутствует, поэтому более точных игровых плиток для замены не найдено. `openItems: 0`, `missingFields: 0`.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Прямой URL возвращает 403, MediaWiki API доступен: Series 4 остаётся текущей; в категории нет новой Autumn-подстраницы. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169617 от 17 августа; API для `Forza Horizon 6/Series 4/Autumn Season` возвращает `missing`, точных Autumn-плиток нет. |
| Official Forza Festival Playlist | Живой HTML доступен с HTTP 200 и подтверждает `Horizon Mascot Party — Autumn`, текущие названия, порядок, условия и награды без поправок. |
| Official Forza News | Статья `Join the Horizon Mascot Party` от 10 августа подтверждает Autumn 20–27 августа; более свежей официальной недельной поправки не опубликовано. |
| Forza Support Release Notes | Help Center API доступен: последними остаются `FH6 Release Notes: August 10, 2026`, обновлённые 13 августа; нового патча нет. |
| Forza Support Known Issues | Help Center API доступен; статья остаётся обновлённой 20 июля и не содержит отдельного официального пункта о текущих Autumn-испытаниях. |
| Official Forza Forums | URL отвечает HTTP 200 общей страницей закрытого форума; свежего официального треда Series 4 Autumn нет. |
| Reddit r/ForzaHorizon | Текущенедельные Autumn tuning/breakdown-публикации и комментарии проверены; новых подтверждённых исправлений условий или кодов после предыдущего аудита нет. |
| Reddit r/ForzaHorizon6 | Полный Autumn guide, отдельный набор тюнингов и комментарии проверены; одиночная жалоба на Photo уже покрывается уточнённым ориентиром, устойчивого нового бага не подтверждено. |
| Reddit r/forza | `Autumn Information Thread — Series 4` и текущенедельные tune-публикации подтверждают дедлайн и условия; новых обязательных исправлений не найдено. |
| Reddit r/ForzaTune | Subreddit доступен, но отдельного свежего FH6 Series 4 Autumn материала в индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | HTTP 200; отдельной актуальной Autumn-публикации или более точного набора карточных изображений не найдено. |
| ForzaLabs Collector Tool | HTTP 200; инструмент доступен, отдельной текущенедельной публикации по Shimanoyama Heat нет. |
| ForzaLabs Interactive Map | HTTP 200; отдельного актуального Autumn-маркера или набора плиток не найдено. |
| Escorenews FH6 | Прямой раздел возвращает 403, но индексируемые материалы Autumn от 20 августа доступны; обновлённое описание Photo уточнило ориентир на картонные фигуры данго рядом со щитами. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200; индексируемого выпуска DungG по Series 4 Autumn не найдено, прошлосезонные материалы не переносились. |

## Ежедневное уточнение — 2026-08-23 06:05 +07:00

- Живая официальная Playlist повторно подтверждает активный `Series 4 — Horizon Mascot Party / Autumn`: сезон действует до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Названия и порядок 14 карточек, семь Daily, условия, награды и максимум 52 очка не изменились; rollover не выполнялся.
- Новых пустых полей и конфликтов нет: `openItems: 0`, `missingFields: 0`. В свежих текущенедельных публикациях сообщества появились дополнительные варианты настроек для Trial и PR Stunts, но они не дают подтверждённого преимущества перед уже опубликованными кодами, поэтому без необходимости рекомендации не заменялись.
- Отдельно проверены `visual` всех 14 карточек: локальные файлы присутствуют, имеют 14 разных SHA-256 и относятся к текущей Autumn-неделе. Итог полноты: `confirmed: 0`, `community: 14`, `preliminary: 0`, `missing: 0`; точных игровых плиток на Fandom по-прежнему нет, поэтому добросовестно помеченные community-визуалы сохранены.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Прямой URL возвращает 403, но MediaWiki API доступен: в категории есть Series 4 и пустая категория Series 5; нового подтверждения смены сезона нет. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169617 от 17 августа; API для `Forza Horizon 6/Series 4/Autumn Season` всё ещё возвращает `missing`, точных Autumn-плиток не появилось. |
| Official Forza Festival Playlist | Живой HTML доступен с HTTP 200 и подтверждает `Horizon Mascot Party — Autumn`, все 14 текущих активностей, условия и награды без поправок. |
| Official Forza News | Материал `Join the Horizon Mascot Party` от 10 августа остаётся актуальным подтверждением Autumn 20–27 августа; новой официальной недельной поправки нет. |
| Forza Support Release Notes | Help Center API доступен: последними остаются `FH6 Release Notes: August 10, 2026`, обновлённые 13 августа; нового патча после старта Autumn нет. |
| Forza Support Known Issues | Help Center API доступен; статья по-прежнему обновлена 20 июля и не содержит отдельного официального пункта о текущих Autumn-испытаниях. |
| Official Forza Forums | URL отвечает HTTP 200 общей страницей закрытого форума; свежего официального треда Series 4 Autumn не найдено. |
| Reddit r/ForzaHorizon | Проверены текущенедельные breakdown/tuning-публикации и комментарии; новый гайд от 21 августа предлагает альтернативы, но не подтверждает ошибку опубликованных кодов. |
| Reddit r/ForzaHorizon6 | Полный Autumn guide и свежие комментарии остаются текущими; новых исправлений условий или отдельных более точных изображений после предыдущего аудита нет. |
| Reddit r/forza | `Autumn Information Thread — Series 4` и свежий tuning guide от 21 августа подтверждают текущую неделю; найденные альтернативные коды не переносились автоматически. |
| Reddit r/ForzaTune | Subreddit доступен, но отдельного свежего FH6 Series 4 Autumn материала в поисковом индексе не найдено; старые настройки не использовались. |
| Forza Horizon Hub | HTTP 200; индекс по-прежнему показывает общий материал Series 1, отдельной актуальной Autumn-публикации или набора плиток нет. |
| ForzaLabs Collector Tool | HTTP 200; инструмент доступен, но отдельной текущенедельной публикации по Shimanoyama Heat не найдено. |
| ForzaLabs Interactive Map | HTTP 200; отдельного актуального Autumn-маркера или набора карточных изображений не найдено. |
| Escorenews FH6 | Прямой раздел отдаёт 403, но индексируемые Autumn Series 4 guide, Weekly, Trial, Photo и Collectibles материалы от 20 августа доступны и подтверждают опубликованные решения. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200; индексируемого выпуска DungG по Series 4 Autumn не найдено, прошлосезонные материалы не использовались. |

## Повторный аудит и замена визуалов — 2026-08-22 06:34 +07:00

- Живая официальная Playlist и статья Series 4 повторно подтверждают активный `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Смена сезона не выполнялась.
- Причина общего изображения найдена: точная Fandom-страница `Forza Horizon 6/Series 4/Autumn Season` всё ещё возвращает `missing`, а прежний workflow разрешал сохранять единый Series fallback до её появления. При этом свежий текущенедельный Reddit-гайд уже содержал отдельные визуалы активностей, но ежедневный запуск не был обязан перепроверять все `visual`, если других изменений не было.
- Выполнен отдельный аудит всех 14 карточек. Десять карточек получили актуальные скриншоты/рендеры непосредственно из полного гайда Series 4 Autumn; Stunt Party получил узнаваемый игровой кадр FH6; для Daily, Hide & Seek и Monthly Rivals сделаны разные явно подписанные квадратные визуалы из актуальной Autumn-инфографики. Все файлы локальные, 720×720, 39–126 КБ; общий `season-fallback.jpg` больше не используется карточками.
- Итог полноты визуалов: `confirmed: 0`, `community: 14`, `preliminary: 0`, `missing: 0`. Точные игровые Fandom-плитки по-прежнему предпочтительнее и будут заменять community-визуалы по мере публикации, но публичных пустых/общих fallback-карточек больше нет.
- В repo skill, `AGENTS.md`, `docs/WORKFLOW.md`, `docs/SOURCES.md`, `docs/WEEKLY_TEMPLATE.md` и в самой automation `fh6` закреплена обязательная ежедневная проверка `visual` каждой карточки независимо от `openItems`. Прошлонедельные изображения запрещены; общий fallback считается только временным состоянием.

| Обязательный источник | Результат повторной проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Прямой сайт отдаёт 403, MediaWiki API доступен; новой Autumn-подстраницы Series 4 в категории не появилось. |
| Forza Wiki / Fandom | API для `Forza Horizon 6/Series 4/Autumn Season` по-прежнему возвращает `missing`; точных Fandom-плиток Autumn нет. |
| Official Forza Festival Playlist | Живой индекс подтверждает `Horizon Mascot Party — Autumn`, 20–27 августа, порядок, условия и награды всех карточек. |
| Official Forza News | Статья `Join the Horizon Mascot Party` от 10 августа доступна и подтверждает Autumn 20–27 августа; новых недельных поправок нет. |
| Forza Support Release Notes | На официальной Support-странице последними остаются `FH6 Release Notes: August 10, 2026`; нового патча после старта Autumn не найдено. |
| Forza Support Known Issues | Страница прочитана; она обновлена 20 июля и не содержит отдельного пункта о текущих Autumn-визуалах или карточках. |
| Official Forza Forums | URL отвечает, но индекс подтверждает закрытие форума 30 июня; свежего официального Autumn-треда нет. |
| Reddit r/ForzaHorizon | Свежие Autumn breakdown и tuning guide проверены; breakdown использован как актуальная сезонная инфографика. |
| Reddit r/ForzaHorizon6 | Полный текущенедельный Autumn guide и его JSON-представление проверены; получены прямые URL отдельных изображений активностей. |
| Reddit r/forza | Autumn Information Thread остаётся свежим подтверждением условий и дедлайна; новых исправлений визуалов нет. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Autumn поста в индексе subreddit не найдено; старые материалы не использовались. |
| Forza Horizon Hub | HTTP 200; главная всё ещё показывает устаревшую Series 1, поэтому сезонные визуалы оттуда не брались. |
| ForzaLabs Collector Tool | HTTP 200; инструмент доступен, но отдельных текущенедельных карточных изображений не публикует. |
| ForzaLabs Interactive Map | HTTP 200; отдельного Autumn-набора плиток не найдено. |
| Escorenews FH6 | Актуальный Autumn Series 4 guide и отдельные материалы Photo/Collectibles остаются доступными через индекс; они подтверждают решения, но не дают полный набор плиток. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200; индексируемого выпуска DungG по Series 4 Autumn не найдено, Summer-визуалы не переносились. |

## Ежедневное уточнение — 2026-08-22 06:00 +07:00

- Живая официальная Playlist по-прежнему подтверждает `Series 4 — Horizon Mascot Party / Autumn` до 27 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). Порядок 14 карточек, 7 Daily, ограничения, награды и максимум 52 очка не изменились.
- MediaWiki API: Series 4 остаётся на revision 169617, а `Forza Horizon 6/Series 4/Autumn Season` всё ещё возвращает `missing`. Точные Autumn-плитки не появились, поэтому 14 `openItems` и компактный официальный текущенедельный fallback сохранены.
- В свежих комментариях r/ForzaHorizon6 подтверждено, что Horizon Solo освобождает стадион от других игроков во время `Homerun`, а перезапуск обновляет талисманы. Опубликованный способ с Horizon Solo и перемоткой уже покрывает более быстрый вариант, поэтому текст карточки не менялся. Отдельные новые жалобы на незасчитывающееся Photo Challenge пока не получили официального Known Issue или устойчивого нового решения.
- Появился свежий Autumn tuning guide в r/ForzaHorizon с альтернативными текущенедельными кодами и заявленной проверкой против Unbeatable AI. Уже опубликованные коды имеют свежие положительные отзывы, включая Trial Supra, поэтому замена без преимущества не выполнялась. Новых подтверждённых исправлений условий, решений или точных визуалов нет; карточки не менялись, но время полной проверки обновляется по ежедневному правилу.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен; категория Series остаётся без новой Autumn-подстраницы Series 4. |
| Forza Wiki / Fandom | Series 4 revision 169617 от 17 августа; точный Autumn Season URL по-прежнему `missing`, сезонных плиток нет. |
| Official Forza Festival Playlist | Живой HTML подтверждает Autumn, дедлайн 27 августа 14:30 UTC, 14 карточек и прежние условия/награды. |
| Official Forza News | Раздел News и статья `Join the Horizon Mascot Party` проверены; новых поправок после материала от 10 августа нет. |
| Forza Support Release Notes | Help Center API: последними остаются `FH6 Release Notes: August 10, 2026`, обновлённые 13 августа; нового патча нет. |
| Forza Support Known Issues | Страница доступна; нового официального пункта про Autumn, туман Trial или незасчитывающееся Photo Challenge нет. |
| Official Forza Forums | URL official-info снова перенаправляет на `forza.net/forums`; свежего официального недельного треда в индексе нет. |
| Reddit r/ForzaHorizon | Проверены Autumn breakdown, свежие комментарии и новый tuning guide от 21 августа; новых обязательных исправлений карточек нет. |
| Reddit r/ForzaHorizon6 | Полный Autumn guide и новые комментарии проверены; подтверждены Horizon Solo/перезапуск для Homerun, но опубликованный быстрый способ уже достаточен. |
| Reddit r/forza | Autumn Information Thread по-прежнему подтверждает дедлайн, 52 очка, 2 очка Hide & Seek и 1 очко Monthly Rivals за сезон; новых поправок нет. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Autumn поста в индексе subreddit не найдено; старые коды не использовались. |
| Forza Horizon Hub | Главная и недельные инструменты доступны с HTTP 200; новых точных Autumn-плиток или более свежего решения нет. |
| ForzaLabs Collector Tool | HTTP 200; отдельной текущенедельной публикации по Shimanoyama Heat нет. |
| ForzaLabs Interactive Map | HTTP 200; нового специального Autumn-маркера, меняющего решение, не найдено. |
| Escorenews FH6 | Раздел напрямую возвращает 403, но индексируемые Autumn guide, Weekly, Trial, Photo и Collectibles материалы остаются доступными и подтверждают опубликованные данные. |
| DungG Seasonal Playlist | Прямой плейлист уводит на YouTube consent; свежего индексируемого выпуска Series 4 Autumn по-прежнему не найдено, Summer-видео не переносилось. |

## Thursday rollover — 2026-08-21 06:08 +07:00

- Живая официальная Playlist подтверждает новый сезон `Series 4 — Horizon Mascot Party / Autumn`: старт 20 августа 2026 года в 14:30 UTC (21:30 Asia/Krasnoyarsk), дедлайн 27 августа в то же время. Перенесены все 14 фактических карточек в игровом порядке: один общий Daily содержит 7 дней. Сумма доступных очков проверена как 52.
- Сезонные награды: 2024 Chevrolet Camaro ZL1 за 20 очков и 2016 Abarth 695 Biposto за 40. Официальный HTML подтверждает для Trial награду `1969 Datsun 2000 Roadster`; официальная обзорная инфографика и один гайд сообщества показывают Fairlady Z '69 — в публичной карточке оставлен первичный HTML-источник. Та же инфографика печатает 3 очка за Hide & Seek и 4 за Monthly Rivals, что противоречит собственному максимуму 52; живые недельные треды подтверждают 2 и 1 очко сезона соответственно.
- Найдены свежие текущенедельные решения для `#DeliciousDango` и `Homerun`, а также 9-значные коды для Weekly, обоих чемпионатов, трёх PR Stunts и Trial. Все советы сообщества явно помечены как не проверенные проектом в игре; старые коды не переносились.
- Fandom ещё не создал страницу `Forza Horizon 6/Series 4/Autumn Season` и не опубликовал точные плитки карточек. Поэтому используется один компактный официальный текущенедельный fallback-визуал, а 14 точных плиток синхронно оставлены в `missingFields` и `openItems`.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Категория и Series 4 проверены через MediaWiki/API; Autumn Season в категории пока отсутствует. |
| Forza Wiki / Fandom | Страница Series 4 доступна, но точный URL Series 4/Autumn Season возвращает отсутствующую страницу; текущенедельных плиток нет. |
| Official Forza Festival Playlist | Живой HTML подтверждает Autumn 20–27 августа, порядок 14 карточек, условия, ограничения, трассы и награды; скачана официальная Autumn-инфографика. |
| Official Forza News | Материал `Join the Horizon Mascot Party` и раздел News проверены; Autumn заявлена на 20–27 августа, более свежей поправки к карточкам нет. |
| Forza Support Release Notes | Help Center API проверен: последними остаются `FH6 Release Notes: August 10, 2026`, обновлённые 13 августа; нового патча после старта Autumn нет. |
| Forza Support Known Issues | Статья `Forza Horizon 6 Known Issues` проверена; она по-прежнему обновлена 20 июля, отдельной записи про Autumn-карточки, туман Trial или Photo Challenge нет. |
| Official Forza Forums | Старый official-info URL перенаправляет на закрытую/общую страницу Forza Forums; свежего официального недельного треда не опубликовано. |
| Reddit r/ForzaHorizon | Свежий `Series 4 Autumn Breakdown and Rewards` проверен; найдены текущенедельные Trial/PR/Weekly коды и сообщения о тумане/невидимых коллизиях в первой гонке Trial. |
| Reddit r/ForzaHorizon6 | Свежий полный Autumn guide проверен; подтверждены фото, collectibles, трассы, коды и практические подсказки. Расхождение награды Trial уступает официальному HTML. |
| Reddit r/forza | Свежий `Autumn Information Thread — Series 4` подтверждает дедлайн, максимум 52, 2 очка Hide & Seek и 1 очко Monthly Rivals за сезон. |
| Reddit r/ForzaTune | Свежего отдельного поста Series 4 Autumn в поисковом индексе не найдено; отсутствие материала не использовалось для переноса прошлых кодов. |
| Forza Horizon Hub | Главная, Festival Playlist и карты доступны; отдельного подтверждённого Autumn-набора плиток или более свежего решения не найдено. |
| ForzaLabs Collector Tool | Инструмент доступен; отдельной текущенедельной публикации по Shimanoyama Heat нет. |
| ForzaLabs Interactive Map | Интерактивная карта доступна; специального Autumn-маркера, превосходящего свежие скриншоты стадиона, не найдено. |
| Escorenews FH6 | Найдены и прочитаны свежий Autumn Series 4 guide и отдельные текущенедельные материалы по `#DeliciousDango`, `Homerun`, Weekly и Trial; ссылки добавлены к соответствующим карточкам. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200; индексируемого выпуска DungG по Series 4 Autumn на момент аудита не найдено. Старый Summer-выпуск не использовался. |

## Предыдущие аудиты — Series 4 Summer

## Ежедневное уточнение — 2026-08-20 06:38 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон: `Series 4 — Horizon Mascot Party / Summer` до 20 августа 2026 года, 14:30 UTC (21:30 Asia/Krasnoyarsk). На момент проверки Autumn ещё не началась, поэтому rollover не выполнялся; порядок 14 карточек и награды Summer не изменились.
- Fandom MediaWiki API: Series 4 остаётся на revision 169617, Summer Season — на revision 169631. В галерее по-прежнему нет отдельных плиток Seasonal Job и Stunt Party, поэтому два безопасных fallback и 2 `openItems` сохранены.
- Найден индексируемый текущенедельный гайд Escorenews от 13 августа. Он независимо подтверждает опубликованные решения и добавляет практические направления: Hakone Turns проще начинать с севера вниз по склону, Kawazu Nanadaru Loop Bridge — с востока на верхнем уровне шоссе. Эти две подсказки добавлены в карточки; альтернативные share codes не заменяли уже подтверждённые текущенедельные настройки.
- Новых официально подтверждённых багов, изменений условий или более надёжных рекомендаций в свежих Reddit-комментариях не найдено. DungG-выпуск `TaW4mju4Rsg` остаётся доступным и подтверждает текущую Summer-неделю.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен: Series 4 остаётся текущей; появилась только пустая категория Series 5, но страницы новой Series и подтверждения смены сезона нет. |
| Forza Wiki / Fandom | Series 4 revision 169617 и Summer revision 169631 без новых правок; точных Seasonal Job и Stunt Party плиток в 51-файловой галерее нет. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; официальный порядок 14 карточек, ограничения и награды без изменений. |
| Official Forza News | Материал `Join the Horizon Mascot Party` проверен: Summer действует до 20 августа, Autumn начинается 20 августа после сброса; новых поправок к Summer нет. |
| Forza Support Release Notes | Help Center API: последними остаются `FH6 Release Notes: August 10, 2026`, обновлённые 13 августа; нового патча или изменения Playlist нет. |
| Forza Support Known Issues | Help Center API: статья `Forza Horizon 6 Known Issues` по-прежнему обновлена 20 июля; нового официального пункта про Summer-карточки нет. |
| Official Forza Forums | Старый URL official-info перенаправляет на Forza.net; поисковый индекс подтверждает закрытие форумов в июне, свежего недельного треда нет. |
| Reddit r/ForzaHorizon | Проверены Summer breakdown, текущенедельный tune-post и свежие комментарии; новых независимо подтверждённых исправлений или кодов нет. |
| Reddit r/ForzaHorizon6 | Полный Summer guide и свежие комментарии проверены; единичная подсказка об обновлении Daily через меню не подтверждает устойчивый баг. |
| Reddit r/forza | Summer Information Thread и его текущенедельный tune-комментарий проверены; дедлайн 20 августа 14:30 UTC и опубликованные условия подтверждены. |
| Reddit r/ForzaTune | Отдельного свежего FH6 Series 4 Summer tune-post в поисковом индексе нет; старые настройки не переносились. |
| Forza Horizon Hub | Главная и карта доступны с HTTP 200; нового текущенедельного материала или точных плиток для двух открытых карточек нет. |
| ForzaLabs Collector Tool | Инструмент доступен с HTTP 200; свежего сезонного решения или отдельной точной плитки не публикует. |
| ForzaLabs Interactive Map | Карта доступна с HTTP 200; нового сезонного маркера, меняющего опубликованные решения, не найдено. |
| Escorenews FH6 | Страница раздела возвращает 403 напрямую, но найден и прочитан индексируемый Summer Series 4 guide от 13 августа; две полезные подсказки направлений добавлены. |
| DungG Seasonal Playlist | Плейлист отвечает HTTP 200; YouTube oEmbed подтверждает текущенедельное видео `TaW4mju4Rsg` от DungG с полным Summer-гайдом. |

## Ежедневный аудит без изменения карточек — 2026-08-19 06:05 +07:00

> Начиная с этого аудита `lastContentUpdate` означает время последней успешной полной проверки обязательных источников. Поэтому timestamp и публичный отчёт обновляются ежедневно даже без изменения фактов карточек; при неполной проверке время не сдвигается.

- Живая официальная Playlist по-прежнему показывает `Series 4 — Horizon Mascot Party / Summer` за 13–20 августа 2026 года; дедлайн остаётся 20 августа в 21:30 Asia/Krasnoyarsk. Нового сезона, изменения порядка 14 карточек, условий или наград не подтверждено.
- Fandom MediaWiki API: Series 4 остаётся на revision 169617, точная Summer Season — на revision 169631 от 17 августа. В сезонной галерее всё ещё нет отдельных плиток Seasonal Job и Stunt Party, поэтому два безопасных Series 4 fallback и соответствующие `openItems` сохранены.
- Найден прямой текущенедельный выпуск DungG `TaW4mju4Rsg` с полным Summer-гайдом и главами Weekly, Daily, Photo, Treasure, чемпионатов, PR Stunts, Seasonal Job, Trial и Monthly Rivals. Он подтверждает уже опубликованный порядок и решения, но не содержит отдельной точной плитки Stunt Party и не даёт причины заменять свежие share codes.
- Свежие недельные треды Reddit повторно проверены. Новых независимо подтверждённых ошибок, решений или более надёжных рекомендаций не появилось; старые и прямо помеченные авторами как ранее созданные коды не переносились. Карточки не изменены, но `lastContentUpdate` установлен в `2026-08-19T06:05:00+07:00`, после чего отчёт пересобран и опубликован как подтверждение актуальности проверки.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API доступен; Series 4 остаётся текущей, новой сезонной страницы после Summer не опубликовано. |
| Forza Wiki / Fandom | Series 4 revision 169617 и Summer revision 169631 без изменений; точных Seasonal Job и Stunt Party плиток в галерее нет. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; официальный порядок 14 карточек, ограничения и награды без изменений. |
| Official Forza News | Раздел News и текущий материал `Join the Horizon Mascot Party` проверены; новых поправок к Summer-неделе нет. |
| Forza Support Release Notes | Последними остаются notes от 10 августа, обновлённые 13 августа: 3.420.696.0 / 1.420.696.0; новых изменений Playlist нет. |
| Forza Support Known Issues | Страница по-прежнему датирована 20 июля и направляет в Feedback Portal; отдельного нового пункта про Summer-карточки нет. |
| Official Forza Forums | Адрес official-info перенаправляет на закрытые форумы; свежего официального недельного треда после закрытия нет. |
| Reddit r/ForzaHorizon | Проверены Summer breakdown, текущенедельный tune-post и свежая лента; подтверждённых исправлений после прошлого аудита нет. |
| Reddit r/ForzaHorizon6 | Проверены полный Summer guide, альтернативный tune-post и обсуждения Stunt Party; событие подтверждено как проходимое, нового устойчивого бага не выявлено. |
| Reddit r/forza | Summer Information Thread и более свежий Series 4 tuning guide проверены; новых фактов, требующих изменения карточек, нет. |
| Reddit r/ForzaTune | В ленте нет отдельного текущенедельного Horizon Mascot Party поста; найденный Trial-код прямо описан как созданный ранее и не использован. |
| Forza Horizon Hub | Сайт доступен, но недельная витрина всё ещё показывает Series 1; текущие сезонные факты из неё не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог из 626 машин; текущенедельных решений или точных плиток Playlist не публикует. |
| ForzaLabs Interactive Map | Интерактивная карта доступна; нового точного сезонного маркера или визуала для двух открытых карточек нет. |
| Escorenews FH6 | Прямой запрос вернул 403; свежего индексируемого гайда Series 4 Summer поиском не найдено. |
| DungG Seasonal Playlist | Прямой плейлист доступен; найден текущенедельный 19-минутный Summer Series 4 guide `https://youtu.be/TaW4mju4Rsg`, подтверждающий уже опубликованные решения. |

## Ежедневное уточнение — 2026-08-18 06:05 +07:00

- Живая официальная Playlist подтверждает прежний активный сезон: `Series 4 — Horizon Mascot Party / Summer`, 13–20 августа 2026 года, дедлайн 20 августа в 21:30 Asia/Krasnoyarsk. Rollover не требуется; порядок 14 карточек, условия и награды не изменились.
- Fandom опубликовал точную страницу `Forza Horizon 6/Series 4/Summer Season`: revision 169631 от 17 августа 18:50 UTC. В её галерее появились актуальные визуалы Photo Challenge, обоих чемпионатов, Time Attack, трёх PR Stunts, Trial и Monthly Rivals.
- Девять новых Fandom-изображений скачаны, обрезаны в квадрат 640×640 и оптимизированы до 38–73 КБ. Эти карточки переведены в `visual: confirmed`; открытыми остаются только Seasonal Job и Stunt Party, для которых точных изображений в сезонной галерее нет. `openItems` уменьшен с 11 до 2.
- Новых подтверждённых решений, багов или более надёжных share codes нет. Единичное сообщение о незасчитанных Air/Time Attack Daily по-прежнему не имеет второго источника или записи в Known Issues.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API: Series 4 и её категория доступны; точная Summer Season теперь опубликована. |
| Forza Wiki / Fandom | Series 4 обновлена до revision 169617, Summer Season — revision 169631; получены девять точных текущенедельных визуалов. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; 14 карточек, ограничения и награды без изменений. |
| Official Forza News | Раздел News и материал Series 4 проверены; новых поправок к текущей Summer-неделе не опубликовано. |
| Forza Support Release Notes | Последними остаются notes от 10 августа, обновлённые 13 августа: версии 3.420.696.0 / 1.420.696.0; новых изменений карточек нет. |
| Forza Support Known Issues | Страница по-прежнему датирована 20 июля и направляет в Feedback Portal; отдельной записи про Summer Playlist или Daily нет. |
| Official Forza Forums | Тег official-info перенаправляет на официальное сообщение о закрытии форумов; свежего недельного треда нет. |
| Reddit r/ForzaHorizon | Текущие Summer breakdown и tune-post остаются последними; новых исправлений или более надёжных кодов не найдено. |
| Reddit r/ForzaHorizon6 | Полный Summer guide проверен; единичное сообщение о Daily остаётся неподтверждённым. |
| Reddit r/forza | Summer Information Thread по-прежнему подтверждает дедлайн, 53 очка и текущие условия; новых содержательных поправок нет. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer tune-post в поисковом индексе нет; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен, но недельная витрина всё ещё показывает Series 1; текущие сезонные факты из неё не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог машин; текущенедельных решений или визуалов Playlist не публикует. |
| ForzaLabs Interactive Map | Карта доступна; нового точного маркера текущего Treasure Hunt или сезонных визуалов нет. |
| Escorenews FH6 | Свежего индексируемого гайда Series 4 Summer не найдено; последние найденные недельные материалы относятся к прежним Series. |
| DungG Seasonal Playlist | Свежего индексируемого выпуска Series 4 Summer не найдено; прямой YouTube-плейлист остаётся ограничен сервисом. |

## Статистика посещений и повторный аудит — 2026-08-17 22:36 +07:00

- Активный сезон не изменился: `Series 4 — Horizon Mascot Party / Summer`, дедлайн 20 августа 2026 года в 21:30 Asia/Krasnoyarsk. Новых подтверждённых фактов карточек после утреннего аудита нет, поэтому `data/current-season.json` и `lastContentUpdate` сохранены без изменений.
- В постоянную конфигурацию проекта добавлен лёгкий внешний SVG-счётчик `hits.sh`: просмотры текущей страницы сегодня и всего, с переходом к публичной расширенной статистике. Endpoint отвечает `200 image/svg+xml`; cookie, iframe и тяжёлая аналитическая библиотека не добавлялись.
- Счётчик учитывает загрузки страницы, а не уникальных людей: повторные открытия и обращения ботов могут увеличивать значение. Это ограничение явно показано пользователю под счётчиком.

| Обязательный источник | Результат повторной проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Series 4 доступна; отдельной актуальной Summer Season с точными плитками по-прежнему нет. |
| Forza Wiki / Fandom | Страница Series 4 остаётся актуальной; нового сезонного revision или точных Summer-визуалов не найдено. |
| Official Forza Festival Playlist | По-прежнему активна `Horizon Mascot Party — Summer` 13–20 августа; порядок и ограничения карточек не менялись. |
| Official Forza News | Новых поправок к материалу Series 4 и текущей Summer-неделе не опубликовано. |
| Forza Support Release Notes | Последним относящимся к Series остаётся обновление от 10 августа; новых изменений Festival Playlist нет. |
| Forza Support Known Issues | Нового официального пункта про текущую Summer Playlist, Treasure Map или Daily не появилось. |
| Official Forza Forums | Свежего официального недельного треда Series 4 Summer в индексе нет. |
| Reddit r/ForzaHorizon | Текущие breakdown и tune-post проверены; новых подтверждённых исправлений карточек нет. |
| Reddit r/ForzaHorizon6 | Текущий Summer guide остаётся последним подробным материалом; единичное сообщение о Daily не получило независимого подтверждения. |
| Reddit r/forza | Summer Information Thread остаётся актуальным; более свежей подтверждённой поправки нет. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer tune-post не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт доступен, но недельная витрина не даёт более свежих текущих данных. |
| ForzaLabs Collector Tool | Каталог доступен; отдельного нового решения текущей сезонной активности нет. |
| ForzaLabs Interactive Map | Карта доступна; нового точного сезонного маркера не найдено. |
| Escorenews FH6 | Свежего индексируемого гайда Series 4 Summer не найдено. |
| DungG Seasonal Playlist | Свежего индексируемого выпуска Series 4 Summer не найдено; прямое открытие YouTube остаётся ограничено сервисом. |

## Ежедневный аудит без изменения карточек — 2026-08-17 07:50 +07:00

- Живая официальная Playlist по-прежнему показывает `Series 4 — Horizon Mascot Party / Summer` за 13–20 августа 2026 года. Дедлайн остаётся 20 августа 14:30 UTC (21:30 Asia/Krasnoyarsk); смены сезона, порядка 14 карточек, условий и наград не подтверждено.
- Fandom MediaWiki API: `Forza Horizon 6/Series 4` остаётся на revision 169227 от 12 августа, а `Forza Horizon 6/Series 4/Summer Season` всё ещё возвращает `missing`. В категории Series 4 по-прежнему только страница серии и категория машин, поэтому 11 точных сезонных визуалов остаются открытыми на безопасных Series 4 fallback.
- Проверен конфликт года награды `Dango Dashes`: строка официальной Playlist сейчас показывает `1962 BMW Isetta 300 Export`, но официальный FH6 Car List содержит только `1957 BMW Isetta 300 Export`; оба подробных свежих гайда r/forza и r/ForzaHorizon6 также указывают 1957. Опубликованное значение `1957` оставлено без изменения, а расхождение Playlist зафиксировано как официальный табличный typo.
- Свежий комментарий 16 августа в r/ForzaHorizon6 сообщает об одном случае незасчитанных Air Skills и Time Attack Daily. Второго независимого сообщения и записи в официальных Known Issues нет, поэтому это не добавлялось в карточку как подтверждённый баг.
- Новых подтверждённых сезонных фактов, точных плиток или более надёжных share codes нет: `data/current-season.json`, `lastContentUpdate` и сгенерированные сезонные файлы не изменялись. Отсутствие свежих публикаций не использовалось для переноса старых решений, изображений или share codes.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API проверен: Series 4 присутствует; в её категории по-прежнему только страница серии и категория машин, точной Summer Season нет. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169227 от 12 августа; точная страница Summer Season возвращает `missing`, новых сезонных плиток нет. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; порядок 14 карточек без изменений. Расхождение `1962` для Isetta сверено с официальным Car List и не перенесено в сводку. |
| Official Forza News | Раздел новостей и материал Series 4 проверены; новых поправок к текущей Summer-неделе после прошлого аудита не опубликовано. |
| Forza Support Release Notes | Последними остаются notes от 10 августа, обновлённые 13 августа 15:05; версии 3.420.696.0 / 1.420.696.0, новых изменений карточек нет. |
| Forza Support Known Issues | Страница проверена; она по-прежнему датирована 20 июля и отправляет в Feedback Portal, отдельной записи про Summer Playlist, Treasure Map или Daily нет. |
| Official Forza Forums | Старый тег official-info по-прежнему перенаправляет на страницу закрытых форумов; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Проверены текущенедельные breakdown и tune-post Series 4 Summer; после прошлого аудита новых исправлений, точных плиток или более надёжных кодов нет. |
| Reddit r/ForzaHorizon6 | Полный Summer guide остаётся актуальным; найден единичный комментарий 16 августа о незасчитанных Daily, недостаточный для подтверждения бага. |
| Reddit r/forza | Summer Information Thread по-прежнему подтверждает дедлайн, 53 очка, условия и `1957 BMW Isetta 300 Export`; новых содержательных поправок нет. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer tune-post в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | Сайт и карта доступны, но недельная витрина всё ещё показывает устаревшую Series 1; сезонные факты из неё не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог машин; решения или точной плитки текущего Treasure Hunt не публикует. |
| ForzaLabs Interactive Map | Карта доступна; маркера или отдельного решения Treasure Hunt Series 4 Summer не найдено. |
| Escorenews FH6 | Прямая страница недоступна веб-инструменту; свежего индексируемого гайда Series 4 Summer не найдено. |
| DungG Seasonal Playlist | Прямое открытие YouTube ограничено сервисом; свежего индексируемого выпуска Series 4 Summer не найдено. |

## Ежедневный аудит без изменения карточек — 2026-08-15 21:45 +07:00

- Живая официальная Playlist по-прежнему показывает `Series 4 — Horizon Mascot Party / Summer` за 13–20 августа 2026 года. Дедлайн остаётся 20 августа 14:30 UTC (21:30 Asia/Krasnoyarsk); смены сезона, порядка 14 карточек, условий и наград не подтверждено.
- Fandom MediaWiki API: `Forza Horizon 6/Series 4` остаётся на revision 169227 от 12 августа, а `Forza Horizon 6/Series 4/Summer Season` всё ещё возвращает `missing`. В категории Series 4 есть только страница серии и категории машин, поэтому 11 точных сезонных визуалов остаются открытыми на безопасных Series 4 fallback.
- Свежие комментарии 15 августа в недельных Reddit-тредах не содержат исправлений условий, точных плиток или более надёжных share codes. Отдельный комментарий о поведении наградного Exocet не относится к прохождению карточек.
- Новых подтверждённых сезонных фактов нет: `data/current-season.json`, `lastContentUpdate` и сгенерированные сезонные файлы не изменялись. Отсутствие свежих публикаций не использовалось для переноса старых решений, изображений или share codes.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | MediaWiki API проверен: Series 4 и её категория присутствуют; точной Summer Season в категории Series 4 нет. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169227; точная страница Summer Season возвращает `missing`, новых сезонных плиток нет. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; официальный порядок и 14 карточек без изменений. |
| Official Forza News | Статья `Join the Horizon Mascot Party in Forza Horizon 6` от 10 августа проверена; Summer по-прежнему указана на 13–20 августа, новых поправок нет. |
| Forza Support Release Notes | Последние notes от 10 августа, обновлённые 13 августа 15:05, остаются актуальными; версии 3.420.696.0 / 1.420.696.0, новых изменений карточек нет. |
| Forza Support Known Issues | Страница проверена; отдельной официальной записи про текущую Playlist, Treasure Map или засчитывание Summer-карточек нет. |
| Official Forza Forums | Старый тег official-info перенаправляет на страницу закрытых форумов; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Проверены текущенедельный tune-post и связанные материалы Series 4 Summer; новых исправлений или точных плиток после прошлого аудита нет. |
| Reddit r/ForzaHorizon6 | Полный Series 4 Summer guide остаётся актуальным; новых подтверждённых исправлений 15 августа не найдено. |
| Reddit r/forza | Summer Information Thread подтверждает дедлайн, 53 очка и текущие условия; новый субботний комментарий не меняет прохождение карточек. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer tune-post в поисковом индексе нет; старые коды не использовались. |
| Forza Horizon Hub | Сайт и карта доступны, но недельная витрина всё ещё показывает устаревшую Series 1; сезонные факты из неё не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог машин; решения или точной плитки текущего Treasure Hunt не публикует. |
| ForzaLabs Interactive Map | Карта доступна; отдельного актуального маркера сундука Series 4 Summer не найдено. |
| Escorenews FH6 | Прямая страница недоступна веб-инструменту; свежего индексируемого гайда Series 4 Summer не найдено. |
| DungG Seasonal Playlist | Прямое открытие YouTube ограничено сервисом; свежего индексируемого выпуска Series 4 Summer не найдено. |

## Ежедневный аудит без изменения карточек — 2026-08-14 21:45 +07:00

- Живая официальная Playlist по-прежнему показывает `Series 4 — Horizon Mascot Party / Summer` за 13–20 августа 2026 года; смены сезона, нового порядка активностей или исправления условий карточек нет.
- Fandom MediaWiki API подтверждает Series 4 revision 169227, но отдельная страница `Forza Horizon 6/Series 4/Summer Season` всё ещё отсутствует. Поэтому 11 открытых точных визуалов остаются на официальных Series 4 fallback; старые плитки не переносились.
- Свежие недельные треды Reddit повторно подтверждают дедлайн 20 августа 14:30 UTC, 53 очка, Trial, Treasure и текущие share codes. Пятничные комментарии подтверждают проходимость PR Stunts на B600, но не дают причины заменять уже опубликованные текущенедельные рекомендации.
- Новых подтверждённых сезонных фактов нет: `lastContentUpdate` и сгенерированные сезонные файлы не изменялись.

| Обязательный источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Категория проверена через MediaWiki API: Series 4 присутствует; отдельной текущей Summer Season нет. |
| Forza Wiki / Fandom | Series 4 остаётся на revision 169227 от 12 августа; запрос точной Summer Season возвращает `missing`. |
| Official Forza Festival Playlist | Активна `Horizon Mascot Party — Summer` 13–20 августа; все 14 карточек, порядок, ограничения и награды без изменений. |
| Official Forza News | Статья `Join the Horizon Mascot Party in Forza Horizon 6` от 10 августа проверена; новых поправок к текущей неделе нет. |
| Forza Support Release Notes | Проверены notes от 10 августа, обновлённые 13 августа: актуальные версии 3.420.696.0 / 1.420.696.0; новых изменений карточек нет. |
| Forza Support Known Issues | Страница обновлена 20 июля и направляет в Feedback Portal; отдельной официальной записи про Treasure Map или текущую Playlist нет. |
| Official Forza Forums | Старый адрес перенаправляет на сообщение о закрытии форумов; свежего официального недельного треда здесь нет. |
| Reddit r/ForzaHorizon | Проверены свежие Summer breakdown, Treasure-комментарий и tune-post; новых исправлений после утреннего обновления нет. |
| Reddit r/ForzaHorizon6 | Полный Series 4 Summer guide и отдельный Treasure thread подтверждают текущие решения; более нового исправления не найдено. |
| Reddit r/forza | Summer Information Thread подтверждает дедлайн, 53 очка, Trial и 1 сезонное очко Monthly Rivals; пятничные ответы подтверждают прохождение PR Stunts. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer поста в поисковом индексе нет; старые tune codes не использовались. |
| Forza Horizon Hub | Сайт и карта доступны, но недельная витрина всё ещё показывает устаревшую Series 1; сезонные факты из неё не брались. |
| ForzaLabs Collector Tool | Инструмент доступен и показывает каталог машин, но не публикует решение текущего сезонного Treasure Hunt. |
| ForzaLabs Interactive Map | Карта доступна; отдельного актуального маркера сундука Series 4 Summer не найдено. |
| Escorenews FH6 | Свежего индексируемого гайда Series 4 Summer не найдено; в выдаче остаются материалы прежних Series. |
| DungG Seasonal Playlist | Плейлист проверен через поиск; индексируемого выпуска Series 4 Summer нет, прямое открытие YouTube ограничено сервисом. |

## Замена favicon и повторный аудит — 2026-08-14 09:08 +07:00

- Постоянный favicon проекта заменён предоставленным пользователем изображением. Подготовлены отдельные PNG 32×32 и Apple Touch Icon 180×180 с прозрачными углами; в `data/project.json` указаны новые имена файлов для обхода браузерного кэша.
- Повторная проверка живых источников не выявила изменений сезонных фактов после ежедневного уточнения в 06:22: официальная Playlist по-прежнему показывает активный `Series 4 — Horizon Mascot Party / Summer` за 13–20 августа, новых исправлений карточек или подтверждённых кодов не опубликовано.

| Обязательный источник | Результат повторной проверки |
|---|---|
| Forza Wiki Category:Series (FH6) | Series 4 доступна; отдельная страница Summer Season всё ещё отсутствует. |
| Forza Wiki / Fandom | Нового сезонного revision после утренней проверки нет. |
| Official Forza Festival Playlist | Активна Series 4 Summer, период 13–20 августа; порядок и ограничения без изменений. |
| Official Forza News | Новых поправок к статье Series 4 после старта сезона нет. |
| Forza Support Release Notes | Релиз от 10 августа остаётся последним относящимся к текущей Series. |
| Forza Support Known Issues | Нового пункта, меняющего прохождение карточек текущей недели, нет. |
| Official Forza Forums | Форум остаётся закрытым; свежего официального недельного треда нет. |
| Reddit r/ForzaHorizon | Текущие breakdown и tune-post без более свежей замены. |
| Reddit r/ForzaHorizon6 | Свежий Summer guide остаётся актуальным; новых исправлений не найдено. |
| Reddit r/forza | Summer Information Thread остаётся актуальным; более свежего уточнения нет. |
| Reddit r/ForzaTune | Свежего отдельного FH6 Series 4 Summer tune-post не найдено. |
| Forza Horizon Hub | Главная всё ещё показывает устаревшую Series 1; сезонные факты не использовались. |
| ForzaLabs Collector Tool | Текущего сезонного Treasure-решения инструмент не публикует. |
| ForzaLabs Interactive Map | Отдельного актуального маркера сезонного сундука не найдено. |
| Escorenews FH6 | Свежего индексируемого гайда Series 4 Summer не найдено. |
| DungG Seasonal Playlist | Свежего индексируемого выпуска Series 4 Summer не найдено. |

## Ежедневное уточнение — 2026-08-14 06:22 +07:00

- Живая официальная Playlist, статья Series 4 и свежие недельные треды по-прежнему подтверждают активный `Series 4 — Horizon Mascot Party / Summer` до 20 августа 2026, 14:30 UTC (21:30 Asia/Krasnoyarsk), 53 очка и 14 карточек.
- Treasure Hunt подтверждён вторым независимым свежим гайдом и прямым скриншотом карты: сундук отмечен в южной части `Shimanoyama Drift Circuit`, у въезда на трассу. Карточка получила точный локальный визуал; поля `solution` и `visual` переведены в `confirmed`.
- Weekly Challenge уточнён: финальное фото 2017 Toyota JPN Taxi требуется у `Tokyo Central Railway Station`. Добавлена подсказка сообщества по повторному разрушению одного автомата через Rewind в Horizon Solo с паузой 3–5 секунд.
- Trial уточнён: требуется браслет Horizon Legend; в категорию Total Buggies & Offroad входят также некоторые Pickups & 4x4s.
- Исправлен год награды `Dango Dashes`: `1957 BMW Isetta 300 Export`, подтверждено свежим Information Thread r/forza. Из публичных рекомендаций удалены формулировки о внутреннем тестировании проекта; статус источника остаётся в полях completeness.
- Fandom-страница `Forza Horizon 6/Series 4/Summer Season` всё ещё отсутствует по MediaWiki API. После добавления точной карты Treasure остаются 11 открытых визуалов с официальным Series 4 fallback.

## Аудит обязательных источников — 2026-08-14

| Источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Категория и Series 4 проверены; отдельная Summer Season всё ещё отсутствует. |
| Forza Wiki / Fandom | MediaWiki API: Series 4 существует и не менялась после 12 августа; запрошенная Summer Season возвращает missing. |
| Official Forza Festival Playlist | Series 4 Summer остаётся активной; порядок, ограничения, награды и 53 очка не изменились. |
| Official Forza News | Статья `Join the Horizon Mascot Party` доступна; новых недельных поправок после старта сезона не опубликовано. |
| Forza Support Release Notes | Release Notes от 10 августа обновлены 13 августа 15:05; подтверждены версии патча и награды Summer, новых изменений 14 августа нет. |
| Forza Support Known Issues | Официальная страница проверена; обновление датировано 20 июля и направляет в Feedback Portal, отдельного пункта про Treasure Map в списке нет. |
| Official Forza Forums | Индекс official-info проверен; форум закрыт 30 июня 2026, поэтому свежего Series 4 недельного треда здесь нет. |
| Reddit r/ForzaHorizon | Breakdown, Treasure-комментарий и текущенедельный tune-post проверены; коды и ограничения остаются актуальными. |
| Reddit r/ForzaHorizon6 | Найден свежий полный Summer guide со вторым подтверждением Treasure, прямой картой и уточнениями Weekly Challenge. |
| Reddit r/forza | Свежий Summer Information Thread подтвердил дедлайн, условия, Trial и правильный год BMW Isetta. |
| Reddit r/ForzaTune | Свежего индексируемого FH6 Series 4 Summer tune-post не найдено; старые коды не использовались. |
| Forza Horizon Hub | Главная и карта проверены; недельная витрина на главной всё ещё показывает устаревшую Series 1, поэтому факты сезона из неё не брались. |
| ForzaLabs Collector Tool | Проверен текущий каталог коллекции; сезонного Treasure Hunt решения инструмент не публикует. |
| ForzaLabs Interactive Map | Карта доступна, но отдельного актуального маркера сезонного сундука не найдено; используется прямой скриншот сообщества. |
| Escorenews FH6 | Прямой запрос вернул 403, а свежий индексируемый гайд Series 4 Summer не найден. |
| DungG Seasonal Playlist | Плейлист проверен через поиск; свежий индексируемый выпуск Series 4 Summer не найден, прямое открытие YouTube было ограничено сервисом. |

## Rollover — 2026-08-13 22:03 +07:00

- Live Forza Festival Playlist и свежая публикация сообщества подтвердили Series 4 `Horizon Mascot Party`, Summer, 13–20 августа 2026, 21:30 Asia/Krasnoyarsk, 53 очка и 14 игровых карточек: Weekly, один Daily из 7 дней, Photo, Treasure, 2 Championships, Time Attack, 3 PR Stunts, Trial, Seasonal Job, Stunt Party и Monthly Rivals.
- Официальные ограничения и награды взяты из Playlist. Свежий Series 4 tune-post от 13 августа дал 6 текущенедельных кодов для обоих чемпионатов, Time Attack, Trial и трёх PR Stunts; имена авторов в публичной сводке не выводятся.
- Treasure: единственный свежий точный комментарий указывает гараж Shimanoyama Circuit и сообщает о неработающем Treasure Map. Прямого скриншота пока нет, поэтому решение остаётся `preliminary` и открытым пунктом.
- Photo: Hokuryu Sunflower Farm подтверждена свежим описанием и прямой точкой Forza Horizon Hub `loc=568823`.
- Точная Fandom-страница `Forza Horizon 6/Series 4/Summer Season` на момент сборки отсутствует. Страница Series 4 существует (revision 169227), подтверждает даты Series и 53 очка каждой недели. Weekly и Daily используют реальные плитки из свежего игрового скриншота; 12 остальных карточек временно используют компактные официальные изображения Series 4 и остаются открытыми на замену точными плитками.
- Арифметика: `5 + 7 + 2 + 3 + 5 + 5 + 3 + 2 + 2 + 2 + 10 + 3 + 3 + 1 = 53`.

## Аудит обязательных источников — 2026-08-13

| Источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki Category:Series (FH6) | Series 4 уже в категории; сезонной подстраницы Summer пока нет. |
| Forza Wiki / Fandom | Series 4 revision 169227 подтверждает `Horizon Mascot Party`, 13.08–10.09 и 53 очка Summer; получены официальные Series 4 assets. |
| Official Forza Festival Playlist | Подтверждены все 14 карточек, порядок, ограничения, трассы и награды Summer. |
| Official Forza News | Актуальная статья Series 4 найдена; её URL и описание подтверждены Series 4 Fandom revision и официальным репостом r/forza. |
| Forza Support Release Notes | Проверен материал обновления от 10 августа; прямой запрос из PowerShell вернул 403, поэтому факты карточек из него не брались. |
| Forza Support Known Issues | Страница доступна веб-поиску; свежая проблема исчезающих discovered roads сопоставлена с сообщением сообщества, но в карточки не добавлялась. |
| Official Forza Forums | Тег official-info проверен; отдельного недельного Festival Playlist thread в индексе не найдено. |
| Reddit r/ForzaHorizon | Найдены свежие breakdown, точка Treasure, подсказки и текущенедельные коды. |
| Reddit r/ForzaHorizon6 | Проверен свежий поток Series 4; отдельного полного Summer guide на момент запуска нет. |
| Reddit r/forza | Найден свежий официальный репост `Join the Horizon Mascot Party`, подтверждающий старт 13 августа 14:30 UTC. |
| Reddit r/ForzaTune | Свежего Series 4 Summer FH6-поста в поисковом индексе не найдено; старые коды не использовались. |
| Forza Horizon Hub | Использованы прямые ссылки на Hokuryu Sunflower Farm и Shimanoyama Circuit. |
| ForzaLabs Collector Tool | Проверен; текущенедельного текстового решения сундука не предоставляет. |
| ForzaLabs Interactive Map | Проверен как альтернативная карта; карточки используют более точные deep links Horizon Hub. |
| Escorenews FH6 | Свежего гайда Series 4 Summer в индексе на момент запуска нет. |
| DungG Seasonal Playlist | Плейлист проверен; отдельный индексируемый выпуск Series 4 Summer на момент запуска не найден. |

## Постоянные правила источников — 2026-08-13

- Канонический обязательный перечень теперь хранится в `data/project.json.requiredSources`, а валидатор требует все 16 записей.
- `docs/SOURCES.md`, `docs/WORKFLOW.md`, repo skill и automation `fh6` требуют датированный аудит каждого источника при каждом запуске. Отсутствие свежего материала фиксируется явно и не разрешает перенос прошлой недели.
- Все ссылки карточек обязаны иметь `target="_blank" rel="noopener noreferrer"`; это проверяется в state и в финальном публичном HTML.

# Предыдущие source notes — 2026-08-09, карточный редизайн

## Ежедневное уточнение — 2026-08-09 21:49 +07:00

- Живая официальная Playlist, новость Series 3, Forza Support Known Issues, Fandom revision 168401 и свежие публикации Reddit по-прежнему подтверждают Series 3 Spring до 13 августа 2026, 14:30 UTC.
- Для `Out of the Loop!` добавлено предупреждение о фактическом фильтре допуска: перед выбором 4Runner нужно установить B600-тюнинг; Ford Bronco R может быть отклонён игрой, несмотря на принадлежность к Offroad. Основной проверенный код `171 532 374` не менялся.
- Нового сезона, новых обязательных карточек и официально подтверждённого сезонного бага в списке Forza Support не найдено.

- Scope: FH6 Series 3 «Italian Exotics», Spring, 2026-08-06 14:30 UTC — 2026-08-13 14:30 UTC.
- Пользовательская поверхность: заголовок, оставшееся время и точное число карточек из `season.expectedCardCount`. Семь Daily объединены в одну карточку; остальные игровые карточки сохранены раздельно и в официальном порядке.
- Удалены Executive Summary, индекс, метрики, диаграмма очков, проверка полноты, общие ловушки, список неопределённостей и ограничения источников.
- `Unknown` в верхней панели был не статусом активности, а пустой датой свежести portable-reader. Исправление: `snapshot.generatedAt` теперь заполняется вместе с `manifest.generatedAt`.
- Официальная Festival Playlist подтверждает названия, ограничения, трассы, очки и награды. Свежие Reddit-публикации текущей недели используются для решений, направлений разгона, автомобилей, авторов и share codes.
- Пользовательский отчёт не показывает статус проверки автомобилей и тюнингов проектом. Автор каждого приведённого share code сохранён рядом с кодом.
- В каждой карточке есть квадратный официальный Spring-визуал и пиктограмма типа активности. Канонический `artifact.json` сохраняет data URI для штатной проверки; публичный HTML загружает оптимизированные локальные файлы из `reports/assets/fandom-spring/`.
- Точные игровые плитки не снимались во время этой итерации: Forza была открыта внутри активного командного заезда, который не прерывался. Ежедневный workflow теперь требует снимать плитки только из безопасного состояния меню.
- Из-за явного требования убрать диаграмму канонический артефакт использует portable surface `dashboard`: валидатор поверхности `report` принудительно требует chart-блок и нарушил бы точное соответствие числу игровых карточек. Это влияет только на внутреннюю проверочную оболочку; пользовательский файл остаётся лёгкой публичной сезонной сводкой.
- Визуальная QA через in-app Browser не выполнена: политика браузера блокирует локальные `file://` URL. Штатная сборка и portable-валидация выполняются отдельно.

## Обновление визуалов и верхней панели — 2026-08-09

- Страница сезона: [Forza Horizon 6/Series 3/Spring Season](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_3/Spring_Season). Имена файлов получены через Fandom MediaWiki API `action=parse`, исходные URL и размеры — через `action=query&prop=imageinfo`.
- В `reports/assets/fandom-spring/` сохранены текущие Spring-иллюстрации карточек и оригинальные игровые пиктограммы типов активностей. Публичная страница обращается к этим файлам по относительным URL и использует ленивую загрузку; запуск игры и ручная съёмка не требуются.
- Для Weekly и объединённой Daily на сезонной Wiki нет отдельных иллюстраций плиток. Вместо малочитаемого общего скриншота Playlist теперь используются разные квадратные визуалы: игровой рендер требуемого 1980 Abarth Fiat 131 из Forza Wiki и официальный арт Italian Exotics с Ferrari из новости Forza. Оба изображения обрезаны до 640×640 и оптимизированы для быстрой загрузки. Для Stunt Party отдельная иллюстрация отсутствует; использован визуал Horizon Life с оригинальной пиктограммой Stunt Party.
- `reports/enhance_portable_html.mjs` после штатной portable-сборки добавляет живой посекундный таймер до ближайшего четверга 21:30 Asia/Krasnoyarsk и подпись `Обновлено:` с `snapshot.generatedAt`. Таймер вычисляется в браузере и не устаревает после публикации.
- После жалобы на зависания тяжёлая оболочка удалена из пользовательского файла полностью: `reports/enhance_portable_html.mjs` собирает одну статическую DOM-страницу без iframe, React-reader и повторных base64-изображений. Карточки имеют естественную высоту; для невидимых ниже экрана блоков используется `content-visibility:auto`.
- Итоговый `current-week.html` уменьшен примерно с 2,63 МБ до 34 КБ. 28 изображений вынесены в отдельные кэшируемые файлы (27 загружаются лениво); canonical `artifact.json` по-прежнему проходит штатные validation/package перед облегчённой сборкой.

## Контур смены сезона и ежедневного дополнения — 2026-08-09

- `data/current-season.json` стал единым редактируемым источником метаданных сезона, порядка карточек, текстов, визуалов, статусов полноты и открытых полей. Текущий Markdown, `artifact.json` и HTML теперь генерируются из него.
- Число карточек, число Daily, дедлайн, папка assets и предельный размер HTML больше не зашиты под Series 3 Spring: их читает state и проверяет `automation/validate_season.ps1`.
- Добавлены repo-навык `$fh6-season-maintainer`, `AGENTS.md`, JSON Schema, безопасный `start_new_season.ps1`, генератор Markdown и архив `data/history/`. Rollover отказывается перезаписывать существующий сезонный архив.
- Ежедневная automation `fh6` явно вызывает навык. В четверг она подтверждает новую Playlist и применяет rollover; в остальные дни работает по `openItems`/`missingFields`. При отсутствии новых данных timestamp и генерируемые файлы не меняются.
- Публикация теперь блокируется при структурной ошибке и после Pages проверяет не только HTML, но и все относительные изображения отчёта.

## Постоянный блок поддержки — 2026-08-09

- Пользователь предоставил QR-файл и ссылку Сбербанка; они сохранены как постоянные проектные данные в `data/project.json` и `reports/assets/project/`, отдельно от сезонного состояния.
- Блок `Сказать Спасибо (поддержать проект)` завершает README и публичный недельный отчёт. Он не входит в количество карточек Festival Playlist.
- QR скопирован без перекодирования; SHA-256: `68C548E7C71C3B972679EAEBB69DEA9BE9A52D2B2F29BED29407A090160735AD`. Ссылка в кнопке проверяется структурным валидатором.
- Требования стандартного executive-report к отдельным сводным разделам здесь намеренно не применяются: пользовательский формат — последовательность игровых карточек без Executive Summary; новая секция является постоянным завершающим действием, а не аналитическим выводом.

## Иконка вкладки и ярлыка — 2026-08-09

- Исторически был добавлен сезонно-независимый ярлык FH6; 13 августа 2026 года он заменён пользовательским PNG-изображением для вкладки и мобильного ярлыка.
- Исходник хранится в `reports/assets/project/`, а пути — в `data/project.json`, поэтому rollover сезона не меняет иконку.
- Визуальный мотив: тёмный квадрат, белая маркировка `FH6` и розово-оранжевый градиент Horizon; официальные логотипы и игровые скриншоты не встраиваются.

## Бейджи класса и PI — 2026-08-09

- `reports/build_artifact.ps1` автоматически превращает текстовые ограничения `D/C/B/A/S1/S2/R/X + три цифры` в компактные бейджи: цветной класс слева, светлый PI справа и небольшой наклон в стиле игрового интерфейса.
- Обработка применяется только к текстовым узлам условия, способа прохождения и рекомендации автомобиля; HTML-теги, ссылки и 9-значные share codes не изменяются.
- Текущая неделя содержит `B600`, `A700` и `S1 800`. Валидатор сравнивает количество готовых бейджей с количеством PI-обозначений в `data/current-season.json`, поэтому новые сезоны получают оформление автоматически.

## Компактность, пиктограммы и данные автомобилей — 2026-08-13

- PI-бейдж уменьшен до высоты строки и поднят на базовую линию текста. Цвет класса и отдельное светлое поле PI сохранены.
- Белые пиктограммы активности теперь лежат на тёмной подложке с лаймовой рамкой: контраст не зависит от толщины белых линий исходной иконки.
- Для каждой конкретной рекомендации добавлен год автомобиля; имена авторов тюнингов удалены, остаются только 9-значные share codes.
- Ссылки из `howHtml` Photo Challenge и Treasure Hunt перенесены в `sourceHtml`, то есть в нижнюю строку карточки.
- Favicon заменён предоставленным пользователем изображением FH6 Season Guide; опубликованы отдельные PNG 32×32 и 180×180 с новыми именами для сброса браузерного кэша.
- Число карточек не считается константой: генератор и валидатор используют только `season.expectedCardCount` текущего состояния.
