# Source notes — 2026-09-07, Series 4 Spring

## Ежедневный аудит перед rollover — 2026-09-10, 06:18 +07:00

- Живая [Festival Playlist](https://forza.net/fh6playlists) уже анонсирует следующий Series `British Automotive` с 10.09, но на момент аудита в Красноярске активная Series 4 Spring ещё не завершилась: сохранённый дедлайн — **10.09.2026 21:30 +07:00**. Поэтому rollover не запускается из предположения по календарной дате.
- Сводка актуальна — содержательных изменений карточек, решений, тюнингов, изображений или `openItems` не требуется. Визуалы проверены: **confirmed=13, community=1, preliminary=0, missing=0**; все 14 подготовленных плиток и их исходники доступны локально.

| Источник | Результат проверки 06:18 +07:00 |
|---|---|
| fandom_series_category | unavailable: HTTP 403; новые данные и визуалы не переносились. |
| fandom_current | unavailable: HTTP 403; сезонные факты из недоступной страницы не добавлялись. |
| forza_playlist | checked: HTTP 200; виден будущий Series, но без основания менять ещё активную Spring до её времени окончания. |
| forza_news | checked: HTTP 200; доступна новость Series 4, новой корректировки Spring нет. |
| forza_support_release_notes | unavailable: configured section HTTP 404; новые факты не добавлялись. |
| forza_support_known_issues | checked: HTTP 200; нового ограничения Spring не найдено. |
| forza_forums_official | no_current_item: HTTP 200, свежей темы Spring нет. |
| reddit_forzahorizon | checked: HTTP 200, конфликтующих коррекций условий/кодов не найдено. |
| reddit_forzahorizon6 | checked: HTTP 200, Spring guide остаётся актуальным; новой отдельной плитки нет. |
| reddit_forza | checked: HTTP 200, конфликтующих недельных данных не найдено. |
| reddit_forzatune | no_current_item: HTTP 200, нового отдельного Spring-поста нет. |
| forza_horizon_hub | no_current_item: HTTP 200, новой публикации Spring-недели нет. |
| forza_labs_collector | no_current_item: HTTP 200, нового решения/визуала нет. |
| forza_labs_map | checked: HTTP 200, карта доступна; текущие плитки проверены локально по sourceImage/image. |
| escorenews_fh6 | unavailable: HTTP 403; материал не использовался. |
| dungg_playlist | no_current_item: HTTP 200, нового индексируемого выпуска Spring нет. |

## Пользовательская плитка Daily и внеплановый аудит — 2026-09-09, 08:10 +07:00

- Пользователь передал игровой скриншот Daily. Оригинал сохранён как `daily-user-screenshot-2026-09-09.png` (612×975, SHA-256 `A81EC6CDD75EB543BDAC83448DB7FD1923CAA745C4D368DEFC4EE16ECA27A96A`); из него без ретуши вырезана только граница активной плитки **«За руль»** — `tile-daily-user-crop.webp` (528×294). Соседние задания, полоса прокрутки и красная пользовательская разметка не попали в подготовленный файл.
- Живые [Festival Playlist](https://forza.net/fh6playlists) и [новость Series 4](https://forza.net/news/forza-horizon-6-series-4) подтверждают, что до rollover остаётся **Series 4 «Horizon Mascot Party» / Весна**. Визуалы: **confirmed=13, community=1, preliminary=0, missing=0**; теперь у всех 14 карточек есть сохранённый исходник и локально подготовленная точная игровая плитка.

| Источник | Результат проверки 08:10 +07:00 |
|---|---|
| fandom_series_category | unavailable: HTTP 403; новые факты, коды и изображения оттуда не брались. |
| fandom_current | unavailable: HTTP 403; для Daily использован только пользовательский игровой скриншот. |
| forza_playlist | checked: HTTP 200; живая Playlist остаётся источником текущей Spring-недели. |
| forza_news | checked: HTTP 200; Series 4 News доступна, rollover по одной локальной дате не применяется. |
| forza_support_release_notes | unavailable: URL раздела вернул HTTP 404; новые Spring-факты не добавлялись. |
| forza_support_known_issues | checked: HTTP 200; нового ограничения для уже записанных карточек не найдено. |
| forza_forums_official | no_current_item: HTTP 200, отдельной свежей темы Spring не найдено. |
| reddit_forzahorizon | checked: HTTP 200; свежих конфликтов с текущими условиями/кодами не найдено. |
| reddit_forzahorizon6 | checked: HTTP 200; текущий Spring guide доступен, отдельной более точной Daily-плитки нет. |
| reddit_forza | checked: HTTP 200; новых конфликтующих недельных данных нет. |
| reddit_forzatune | no_current_item: HTTP 200, нового отдельного Spring-поста нет; старые коды не переносились. |
| forza_horizon_hub | no_current_item: HTTP 200, новой публикации Spring-недели нет. |
| forza_labs_collector | no_current_item: HTTP 200, отдельной Daily-плитки или решения не опубликовано. |
| forza_labs_map | checked: HTTP 200; карта доступна, но визуал взят из точного игрового скриншота. |
| escorenews_fh6 | unavailable: HTTP 403; материал не использовался. |
| dungg_playlist | no_current_item: HTTP 200, нового индексируемого выпуска Spring не найдено. |

## Внеплановый аудит и исправление мобильной читаемости — 2026-09-09, 06:39 +07:00

- Живые [Festival Playlist](https://forza.net/fh6playlists), [новость Series 4](https://forza.net/news/forza-horizon-6-series-4) и [ForzaLabs Series Details](https://forza.labsgg.com/series/details) повторно подтверждают активную **Series 4 «Horizon Mascot Party» / Весна** до **10.09.2026 21:30 Asia/Krasnoyarsk**: 14 карточек и один Daily из 7 пунктов. Сводка актуальна — содержательных изменений условий, решений, кодов, наград или порядка не требуется.
- Вложенный мобильный скриншот выявил CSS-конфликт: настольное правило `.card-vertical .wrap` было специфичнее общего mobile-правила и сохраняло две колонки. В мобильном breakpoint теперь явно задаётся одна колонка и для вертикальных карточек; плитка располагается над текстом, базовый текст — 16 px с увеличенным межстрочным интервалом. Добавлен регрессионный тест, чтобы конфликт не вернулся.
- Визуалы проверены для всех 14 activity: **confirmed=13, community=0, preliminary=0, missing=1**. `activity_02_daily` по-прежнему не имеет отдельной точной игровой плитки в обязательных источниках; общий или старый fallback не применяется. Очередь запроса оригинального полного скриншота: `automation/runs/visual-evidence-queue.json`.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория Series](https://forza.fandom.com/wiki/Category:Series_(FH6)) не открылась в reader; старые решения, коды или плитки не переносились. |
| fandom_current | unavailable: [Spring Season](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) недоступна reader; отдельная Daily-плитка не получена. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) подтверждает Spring, 14 карточек, 7 Daily, условия, порядок и награды. |
| forza_news | checked: [Series 4 News](https://forza.net/news/forza-horizon-6-series-4) подтверждает текущую Spring; опубликованный Series 5 ещё не используется как активный сезон. |
| forza_support_release_notes | unavailable: актуальная [страница Release Notes](https://support.forza.net/hc/en-us/articles/55121247584915-FH6-Release-Notes-September-7-2026) дала reader internal error; из неё не брались новые факты Spring. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) доступны; нового Spring-ограничения нет. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) перенаправляет на объявление о закрытии; свежего weekly-треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) подтверждает порядок; свежие комментарии подтверждают уже используемые community-коды, замены не потребовались. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) проверен; новых конфликтующих решений или отдельной Daily-плитки нет. |
| reddit_forza | checked: [Spring Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) остаётся актуальным для текущей недели. |
| reddit_forzatune | no_current_item: в [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) не найден отдельный свежий пост именно для Series 4 Spring; старые коды не добавлялись. |
| forza_horizon_hub | no_current_item: [Forza Horizon Hub](https://forzahorizonhub.com/) доступен, но не публикует свежий материал этой Spring-недели. |
| forza_labs_collector | no_current_item: [Collector Tool](https://forza.labsgg.com/collector-tool) проверен; отдельного решения Spring Treasure/Collectibles не публикует. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) доступны; Details подтверждает 13 точных отдельных плиток, но не Daily. |
| escorenews_fh6 | unavailable: [индекс FH6](https://escorenews.com/en/games/forza-horizon-6) недоступен reader; материал не использовался. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) throttled; старые видео не переносились. |

## Внеплановый полный аудит и улучшения отчёта — 2026-09-09, 00:18 +07:00

- Живая [официальная Playlist](https://forza.net/fh6playlists), [новость Series 4](https://forza.net/news/forza-horizon-6-series-4) и [Series Details](https://forza.labsgg.com/series/details) подтверждают активную **Series 4 «Horizon Mascot Party» / Весна** до **10.09.2026 21:30 Asia/Krasnoyarsk**: 14 карточек, один Daily из 7 пунктов и 53 очка. Официальная [новость Series 5](https://forza.net/news/forza-horizon-6-series-5) и Release Notes указывают, что следующий Series стартует 10.09; переключение по одной только дате не выполнялось.
- Для Daily обновлена оперативная подсказка: в 00:18 09.09 доступны пункты 03–08.09, последний открывается в 21:30. Новых условий, наград, кодов или порядка карточек не найдено.
- [Release Notes 07.09](https://support.forza.net/hc/en-us/articles/55121247584915-FH6-Release-Notes-September-7-2026) ретроактивно засчитывают **Winter** Daily из-за Horizon Story. Это не заменяет и не отменяет текущие Spring Daily; текущие карточки не менялись по этому исправлению.
- Визуальный аудит выполнен для всех 14 карточек: **confirmed=13, community=0, preliminary=0, missing=1**. У `activity_02_daily` источники показывают семь заданий, но не отдельную точную игровую плитку: старый производный композит удалён из state и не будет опубликован. Требуется неизменённый скриншот с полностью видимой Daily-плиткой; оригинал будет сохранён, а затем из него без ретуши вырежется только граница плитки. Локальная очередь: `automation/runs/visual-evidence-queue.json`.
- В отчёт добавлены компактные статусы происхождения, локальные отметки выполнения/фильтр и копирование 9-значных кодов; они работают в браузере пользователя и не отправляют игровую статистику. В финальном блоке поддержки добавлена нативная SVG-диаграмма последних публичных метрик из versioned истории, без iframe и внешней библиотеки.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория Series](https://forza.fandom.com/wiki/Category:Series_(FH6)) блокируется robots.txt в доступном reader; отсутствие не стало причиной переносить старые решения, коды или визуалы. |
| fandom_current | unavailable: [страница Series 4 Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) недоступна reader; из неё не взяты новые данные и не получена отдельная плитка Daily. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) подтверждает S04 Spring, все 14 карточек, 7 Daily, порядок, условия, награды и окно 03–10.09. |
| forza_news | checked: [Series 4 News](https://forza.net/news/forza-horizon-6-series-4) подтверждает Spring до 10.09; [анонс Series 5](https://forza.net/news/forza-horizon-6-series-5) подтверждает ближайший rollover, но ещё не новую активную Playlist. |
| forza_support_release_notes | checked: [Release Notes 07.09](https://support.forza.net/hc/en-us/articles/55121247584915-FH6-Release-Notes-September-7-2026) доступны; текущий Spring-порядок не изменён, Winter Daily исправлены ретроактивно. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) доступны; свежего отдельного ограничения Spring там нет. |
| forza_forums_official | no_current_item: [официальный тег](https://forums.forza.net/tag/official-info/1731) не дал свежего недельного Spring-треда; отдельная страница Playlist Hub остаётся единственным официальным источником условий. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) текущей недели подтверждает порядок и community-рекомендации; новых замен кодов не найдено. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) подтверждает Series 4 Spring, 7 Daily и дедлайн; отдельной точной Daily-плитки не опубликовано. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) подтверждает текущую неделю; [репост Release Notes](https://www.reddit.com/r/forza/comments/1w9yh7c/fh6_release_notes_september_7_2026/) подтверждает Winter-only исправление. |
| reddit_forzatune | no_current_item: в [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) не найден отдельный свежий FH6 Series 4 Spring-пост; старые коды по этой причине не добавлялись. |
| forza_horizon_hub | no_current_item: [Forza Horizon Hub](https://forzahorizonhub.com/) доступен, но его витрина всё ещё показывает Series 1; факты текущей Spring оттуда не брались. |
| forza_labs_collector | no_current_item: [Collector Tool](https://forza.labsgg.com/collector-tool) проверен; отдельного Spring Treasure/Collectibles-решения не публикует. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) проверены; Series Details показывает отдельные точные плитки 13 activity, но не отдельную плитку Daily. |
| escorenews_fh6 | unavailable: [индекс FH6](https://escorenews.com/en/games/forza-horizon-6) не открылся в доступном reader; свежего индексируемого Spring-материала не использовано. |
| dungg_playlist | unavailable: [DungG Seasonal Playlist](https://www.youtube.com/@DungG) не отдал доступный текущенедельный выпуск в reader; решения, коды и визуалы из прошлых видео не переносились. |

## Контроль Daily после публикации — 2026-09-08, 07:26 +07:00

- При cache-busted просмотре опубликованной сводки обнаружена устаревшая динамическая фраза Daily: она описывала 07.09, хотя сегодня 08.09. Исправлено состояние: доступны 03–07.09, задача 08.09 откроется в 21:30 по Красноярску. Список семи Daily, условия Playlist, порядок, карты, коды, активный сезон и визуалы не менялись.
- Весь набор 16 источников и 14 visual остаётся подтверждённым аудиторскими доказательствами 07:17–07:20 +07:00 этого же запуска; повторная сборка ниже фиксирует корректное оперативное время. Визуалы: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**.

## Внеплановое выравнивание вертикальных плиток и ежедневный аудит — 2026-09-08, 07:18 +07:00

- Живая [официальная Playlist](https://forza.net/fh6playlists) и [ForzaLabs Series Details](https://forza.labsgg.com/series/details) подтверждают активную Series 4 «Horizon Mascot Party» / Весна до **10.09.2026 21:30 по Красноярску**: 14 карточек, один Daily из 7 заданий и 53 очка. Условия, порядок и награды не изменились.
- На широком экране вертикальные точные плитки теперь используют отдельную левую колонку до 280 px и уменьшенный отступ к тексту; горизонтальные плитки и мобильное расположение над текстом не менялись. Это правка вёрстки, не игровых изображений.
- [Свежий current-week breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) повторно подтверждён 08.09. Его непроверенные в игре рекомендации заменили пять устаревших: Unlimited Buddies — 2020 Jimco `481 655 671`; Hot Hatch Chasers и Edamame Time Attack — 2010 Renault Megane RS 250 `119 705 910`; Ito Straight — 2025 GR GT Prototype `140 337 609`; Seaside Trail — 1994 Subaru Vivio RX-R `636 022 410`; Trial — 2022 Lamborghini Huracán Sterrato `170 628 219`. Официальный [список автомобилей](https://forza.net/fh6cars?pubDate=20260124) подтверждает год и название 2025 GR GT Prototype. Эти советы остаются помечены как сообщества — без проверки в игре.
- Визуалы всех 14 activity повторно сопоставлены с текущей Spring: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**. 13 подготовленных файлов соответствуют отдельным игровым плиткам Series Details. Daily остаётся честно помеченным current-week community-композитом из семи игровых Daily, поскольку отдельной плитки активности не опубликовано; это не универсальный или прошлосезонный fallback.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория Series](https://forza.fandom.com/wiki/Category:Series_(FH6)) не открылась в web-reader; недоступность не стала основанием переносить старые решения, коды или визуалы. |
| fandom_current | unavailable: [Spring Season](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) не открылась в web-reader; из недоступной страницы не взяты новые данные. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) подтверждает S04 Spring, 14 активностей, 7 Daily, условия, порядок и награды. |
| forza_news | checked: [Series 4 News](https://forza.net/news/forza-horizon-6-series-4) подтверждает окно Spring 03–10.09; новой корректировки текущей Playlist не найдено. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) не отдал доступный текущенедельный материал в web-reader; факты Spring из него не применялись. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) доступны; нового публичного ограничения Spring не найдено. |
| forza_forums_official | no_current_item: [официальный форум](https://forza.net/forums) перенаправляет на сообщение о закрытии; свежего недельного треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) текущей недели подтверждает условия и даёт свежие community-коды; они обновлены в state без имён авторов. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) проверен: порядок, решения и 7 Daily совпадают с Playlist; противоречий нет. |
| reddit_forza | checked: [Spring Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) подтверждает текущую неделю, 53 очка и смену Playlist 10.09 в 14:30 UTC. |
| reddit_forzatune | no_current_item: в [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) не найден отдельный свежий FH6 Series 4 Spring-пост; старые коды не переносились по этой причине. |
| forza_horizon_hub | no_current_item: [Forza Horizon Hub](https://forzahorizonhub.com/) доступен, но сезонная витрина относится к Series 1; её данные не использовались. |
| forza_labs_collector | no_current_item: [Collector Tool](https://forza.labsgg.com/collector-tool) доступен, но отдельного current-week Collectibles-решения для Spring не публикует. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) доступны; Series Details подтверждает Spring и источники 13 точных игровых плиток. |
| escorenews_fh6 | unavailable: [Escorenews FH6](https://escorenews.com/en/games/forza-horizon-6) вернул ошибку в web-reader; недоступный материал не использовался как доказательство. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) был throttled; подтверждённый выпуск Spring из него не применялся. |

## Ежедневный аудит и переработка плиток — 2026-09-08, 06:50 +07:00

- RunId: `fh6-20260908-063942-377834`. Живая [официальная Playlist](https://forza.net/fh6playlists) (строки S04 Spring 341–359) и [ForzaLabs Series Details](https://forza.labsgg.com/series/details) подтверждают активную Series 4 «Horizon Mascot Party» / Весна до **10.09.2026 21:30 по Красноярску**: 14 карточек, один Daily из 7 заданий и 53 очка. Условия, порядок, награды, решения, рекомендации машин и share codes не менялись.
- [Release Notes от 07.09](https://support.forza.net/hc/en-us/articles/55121247584915-FH6-Release-Notes-September-7-2026) относятся к обновлению Series 5, доступному с 10.09. Для текущей Spring подтверждена только будущая ретро-награда Winter Daily; это не меняет сегодняшние карточки. В Known Issues не найдено нового ограничения Spring.
- Визуалы проверены по 14 отдельным current-week assets и сопоставлены с актуальным Series Details: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**. Исходник каждой карточки сохранён в `visual.sourceImage`; подготовленный `visual.image` убирает только однородную экспортную рамку и не обрезает игровое содержимое. Выявлены два реальных формата: вертикальные Weekly, Photo, Treasure и Trial; горизонтальные Championships, Time Attack, PR Stunts, Horizon Play, Eliminator, Stunt Party и Monthly Rivals. Daily остаётся честно отмеченным community-визуалом из актуальных семи Daily, поэтому не выдаётся за отсутствующую отдельную игровую плитку.
- Оверлеи, затемнение и чёрная квадратная подложка удалены. Значок появляется только в строке типа и очков, с фиксированным размером 24 px, а номер теперь находится у названия. Это изменение представления, не изменение игровых фактов.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) не открылась в web-reader; новых фактов из недоступной страницы не использовано. |
| fandom_current | unavailable: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) не открылась в web-reader; это не стало основанием переносить старые изображения или решения. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — S04 Spring 341–359 подтверждают все 14 активностей, 7 Daily, ограничения, награды и порядок. |
| forza_news | no_current_item: [News](https://forza.net/news) доступен, но новой самостоятельной публикации Series 4 Spring в ленте не найдено; сезон подтверждён Playlist. |
| forza_support_release_notes | checked: [Release Notes 07.09](https://support.forza.net/hc/en-us/articles/55121247584915-FH6-Release-Notes-September-7-2026) — выпуск Series 5 вступает в силу 10.09; текущую Spring не изменяет. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — доступна страница и ссылка на свежий release notes; нового ограничения Spring нет. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) редиректит на объявление о закрытии; свежего недельного треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) текущей недели подтверждает порядок и условия; свежие комментарии не потребовали менять state. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) от 03.09 подтверждает 7 Daily, Photo, Treasure, машины и коды; новых конфликтующих рекомендаций нет. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) подтверждает 53 очка и смену Playlist 10.09 в 14:30 UTC. |
| reddit_forzatune | no_current_item: поиск не нашёл свежего отдельного FH6 Series 4 Spring-поста в [r/ForzaTune](https://www.reddit.com/r/ForzaTune/); старые коды не переносились. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) доступен, но недельный блок всё ещё указывает Series 1; сезонные факты не использовались. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) доступен; отдельной Collectibles-активности Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) доступна; текущая сезонная точка не добавлена как отдельный marker. [Series Details](https://forza.labsgg.com/series/details) подтверждает текущую Spring и отдельные игровые плитки. |
| escorenews_fh6 | unavailable: [Escorenews FH6](https://escorenews.com/en/games/forza-horizon-6) не открылся в web-reader; недоступный материал не использовался как доказательство. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) был throttled; выпуск текущей Spring не применялся без проверки. |

## Внеплановая синхронизация оверлеев — 2026-09-07, 22:14–22:27 +07:00

- RunId: `fh6-20260907-221420-259358`. Живая [официальная Playlist](https://forza.net/fh6playlists) и [ForzaLabs Series Details](https://forza.labsgg.com/series/details) подтверждают Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**: 14 карточек, один Daily из 7 заданий и 53 очка. Новых условий, решений, машин, share codes, порядка или багов засчитывания не найдено.
- Для каждой из 14 исходных Spring-плиток проверен именно значок в её правом верхнем углу. Новый контракт `visual.overlayIconKey` выводит наложение только для 10 плиток, где такой знак есть: Photo, Treasure, два Championships, Time Attack, Speed Trap, Drift Zone, Trial и Monthly Rivals; Horizon Play — единственное явное исключение. Weekly, Daily, Eliminator и Stunt Party остаются без оверлея. Значки двух Championships и Time Attack однократно извлечены из уже сохранённых точных плиток; остальные помещены в постоянную локальную библиотеку `reports/assets/activity-icons/`. При будущих неделях они будут выбираться ключом типа активности, без повторного скачивания.
- Visual audit: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**. 13 отдельных карточек ForzaLabs остаются точными игровыми Spring-плитками. Daily по-прежнему является честно помеченным производным текущенедельным визуалом, а не выданной за игровую плитку.
- Часть обязательных источников оказалась устаревшей или технически недоступной; это зафиксировано ниже и не использовалось для переноса старых решений, изображений либо кодов.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — web-reader не получил страницу; новых фактов из Fandom не использовано. |
| fandom_current | unavailable: [Fandom](https://forza.fandom.com/) — HTTP 402 в web-reader; источник не использовался для изменений. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — строки S04 Spring 341–359 подтверждают текущие названия, 7 Daily, ограничения, награды и порядок. |
| forza_news | no_current_item: [News](https://forza.net/news) — раздел доступен, но свежей отдельной Series 4 Spring-публикации в ленте не найдено; активность сезона подтверждена Playlist. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — web-reader отказался открывать раздел; новых Spring-изменений не применялось. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — страница доступна, свежего ограничения для активностей Spring не опубликовано. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — редирект на объявление о закрытии форума; текущенедельного Festival Playlist-треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) — свежая публикация сверяет 53 очка, порядок, условия и текущенедельные решения; новых противоречий state нет. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) и [Spring tunes](https://www.reddit.com/r/ForzaHorizon6/comments/1w6hnou/series_04_week_4_spring_seasonal_tunes_mascot/) — свежие материалы недели просмотрены; новые коды не заменяли уже подтверждённые рекомендации без конфликта. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — текущая Spring-ветка проверена; новых фактов, требующих правки карточек, нет. |
| reddit_forzatune | no_current_item: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — лента доступна, но отдельного свежего FH6 Series 4 Spring-поста не найдено; старые коды не использованы. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — сайт доступен, но его недельный блок всё ещё относится к Series 1, не к текущей Spring. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — отдельной Collectibles-активности в Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — карта доступна; Series Details показывает текущую Spring и 13 точных локальных плиток. |
| escorenews_fh6 | checked: [Photo-гайд](https://escorenews.com/en/article/80887-peasinapod-photo-challenge-in-spring-series-4-of-forza-horizon-6-festival-playlist-where-is-edamame-area-at-the-mascot-party) — свежий материал 03.09 подтверждает зону Edamame; новых противоречий нет. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — запрос throttled; свежий выпуск не использовался как доказательство. |

## Внеплановое исправление иконок — 2026-09-07, 22:02–22:05 +07:00

- RunId: `fh6-20260907-220209-698244`. Официальные живая Playlist и Series News по-прежнему подтверждают Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**: 14 карточек, один Daily из 7 заданий и 53 очка. Изменений условий, решений, машин, share codes, порядка или файлов визуалов не найдено.
- Исправлен только постоянный слой отображения иконок в генераторе. Причина дефекта: часть локальных исходных иконок уже цветная, а часть белая на чёрном фоне; общий red CSS-filter перекрашивал весь непрозрачный квадрат. Фильтр удалён. Теперь сохраняется исходный игровой цвет каждой иконки, а чёрный фон смешивается с плиткой через `screen`, без отдельной подложки.
- Все 14 visual повторно сверены по локальным SHA-256 и текущим Spring-источникам: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**. Файлы плиток не менялись и не заменялись.
- Прямой браузерный просмотр локального HTML недоступен по политике `file:`; это не обходилось. Исправление проверено по исходным PNG и сгенерированному DOM/CSS, после чего будет выполнена штатная structural/package-проверка.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — HTTP 403; свежие данные из недоступной страницы не использовались. |
| fandom_current | unavailable: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — HTTP 403; существующий Daily-визуал остаётся честно помеченным community. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — HTTP 200; активные Spring-строки соответствуют state. |
| forza_news | checked: [Series 4](https://forza.net/news/forza-horizon-6-series-4) — HTTP 200; Spring 03–10.09 и следующий rollover подтверждены. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — HTTP 404; новый Spring-патч не подтверждён. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — HTTP 200; нового публичного ограничения Spring нет. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — HTTP 200 закрытого архива; текущенедельного треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) — текущая разборка недели сверена, новых исправлений нет. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — текущий гайд и решения остаются актуальны. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — 53 очка и дедлайн 10.09 14:30 UTC подтверждены. |
| reddit_forzatune | no_current_item: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — HTTP 200, но свежей Series 4 Spring-публикации нет; старые коды не переносились. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — HTTP 200, текущего Spring-материала нет. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — HTTP 200; Collectibles-активность отсутствует в Spring. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — HTTP 200; 13 точных Spring-плиток соответствуют текущим локальным files. |
| escorenews_fh6 | unavailable: [Escorenews FH6](https://escorenews.com/en/games/forza-horizon-6) — HTTP 403; недоступные материалы не использовались как доказательство. |
| dungg_playlist | no_current_item: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — HTTP 200 оболочки без читаемого свежего Spring-выпуска. |

## Внеплановое визуальное уточнение — 2026-09-07, 20:50–21:20 +07:00

- RunId: `fh6-20260907-205055-385612`. Живые официальные Playlist и Series News вновь подтверждают активный сезон: Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**. Состав остаётся прежним: 14 карточек, один Daily из 7 заданий, 53 очка.
- **Сводка по фактам актуальна:** условий, решений, машин и share codes менять не потребовалось. Оперативная подсказка Daily на момент проверки остаётся точной: доступны задания 03–06.09, задание 07.09 откроется в 21:30.
- Визуалы всех 14 активностей сверены. 13 отдельных локальных плиток остаются точными игровыми Spring-плитками из ForzaLabs; уникальный Daily-визуал остаётся производным из семи иконок Fandom текущей Spring-недели, не выдан за игровую плитку. Итоги: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**. В генераторе изменено только постоянное размещение: увеличенная тематическая иконка — справа сверху, номер — компактным счётчиком C слева снизу. Файлы карточек не подменялись и не переносились из прошлого сезона.
- Недоступность Fandom, Release Notes и Escorenews в этом запуске записана как проверенный факт и не использовалась как основание переносить старые решения, изображения или коды.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | unavailable: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — прямой запрос вернул HTTP 403, web-reader заблокирован robots.txt; свежие факты из неё не переносились. |
| fandom_current | unavailable: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — прямой запрос HTTP 403 и web-reader robots.txt; используемый ранее явно подписанный community Daily-визуал не выдаётся за игровую плитку. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — HTTP 200; строка поиска направляет к `Horizon Mascot Party - Spring`, а текущие 14 активностей и Daily соответствуют state. Верхняя плашка Winter отстаёт. |
| forza_news | checked: [Series 4](https://forza.net/news/forza-horizon-6-series-4) — HTTP 200; Spring 03–10.09 и награды 20/40 очков подтверждены. Отдельная новость Drift Attack анонсирует следующую Series только на 10.09. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — раздел теперь отвечает HTTP 404; нового проверяемого Spring-патча не найдено. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — HTTP 200; нового публичного ограничения Spring не найдено. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — HTTP 200 ведёт к закрытому архиву; свежего треда Festival Playlist нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) — свежая разбивка 03.09 вновь найдена, новых исправлений условий/кодов нет. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — свежий гайд 03.09 подтверждает Spring 03–10.09, 7 Daily, Photo/Treasure и текущие условия; новых точных плиток Daily нет. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — свежий тред подтверждает 53 очка и смену Playlist 10.09 в 14:30 UTC. |
| reddit_forzatune | no_current_item: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — лента HTTP 200, но свежего Series 4 Spring FH6-поста не найдено; старые коды не переносились. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — HTTP 200, но опубликованная недельная часть не относится к текущей Spring-неделе. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — HTTP 200; отдельной Collectibles-активности в Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — HTTP 200; Spring указан текущим, 13 отдельных точных игровых плиток продолжают соответствовать локальным assets, отдельной Daily-плитки нет. |
| escorenews_fh6 | unavailable: [Escorenews FH6](https://escorenews.com/en/games/forza-horizon-6) — прямой запрос HTTP 403; новые факты из недоступного тела статьи не брались. |
| dungg_playlist | no_current_item: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — оболочка HTTP 200, но читаемого подтверждённого выпуска текущей Spring-недели не найдено. |

## Ежедневное уточнение — 2026-09-07, 06:02–06:09 +07:00

- RunId: `fh6-20260907-060225-541935`. Официальная живая Playlist и Series News подтверждают активный сезон: Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**. Состав остаётся прежним: 14 карточек, один Daily из 7 заданий, 53 очка.
- **Сводка актуальна — содержательных изменений условий, решений, машин или share codes не требуется.** Оперативная подсказка Daily обновлена: утром 07.09 доступны задания 03–06.09, задание 07.09 откроется в 21:30.
- Закрыт единственный visual open item. Fandom теперь отдаёт полноценную страницу Spring (45 изображений), включая семь точных текущенедельных иконок ежедневных заданий. Из них и актуального Spring-обзора собран отдельный локальный квадратный визуал Daily; это явно помеченный производный материал Fandom, а не выданная за существующую игровая Daily-плитка. Итоги визуалов: **confirmed=13, community=1, preliminary=0, missing=0**; **openItems=0**.
- Недоступные или устаревшие площадки перечислены ниже; ни одна из них не использовалась для переноса старых решений, изображений или кодов.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | checked: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — MediaWiki API HTTP 200; список серий проверен. |
| fandom_current | checked: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — страница создана и отдаёт 45 изображений; условия Spring и семь Daily подтверждены. Отдельной игровой Daily-плитки не опубликовано. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — строки S04 Spring содержат текущие 14 активностей и все семь Daily; верхний Winter-заголовок отстаёт. |
| forza_news | checked: [Series 4](https://forza.net/news/forza-horizon-6-series-4) — Spring и окно 03–10.09, а также награды 20/40 очков подтверждены. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — раздел и прямая статья отдают 403; нового подтверждённого Spring-патча не найдено. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — публичная страница доступна; новых публичных ограничений Spring нет. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — редирект на закрытие форума; свежего треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) и Spring Tuning Guide — свежие условия и обсуждения просмотрены, новых исправлений нет. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — условия, карты и актуальные обсуждения сверены; новый отдельный Daily-кадр не найден. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — 53 очка, дедлайн 10.09 14:30 UTC и все активности подтверждены. |
| reddit_forzatune | unavailable: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — live `new.json` вернул HTTP 403; проверяемого нового Spring-поста не найдено. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — сайт доступен, но показывает Series 1, не текущую Spring-неделю. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — каталог доступен; отдельной Collectibles-активности в Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — карта доступна; Series Details подтверждает Spring, 13 точных отдельных игровых плиток и отсутствие Daily-плитки. |
| escorenews_fh6 | checked: [Spring guide](https://escorenews.com/en/article/80890-spring-series-4-weekly-festival-playlist-guide-in-forza-horizon-6-best-tunes-to-complete-challenges-in-fh6) и [Treasure](https://escorenews.com/en/article/80888-tokyo-city-region-treasure-hunt-in-forza-horizon-6-spring-series-4-treasure-chest-location) — свежие статьи 03.09 доступны и подтверждают опубликованные решения. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — оболочка HTTP 200, но читаемого подтверждённого списка свежих выпусков нет. |

# Source notes — 2026-09-06, Series 4 Spring

## Ежедневное уточнение — 2026-09-06, 06:01–06:04 +07:00

- RunId: `fh6-20260906-060115-092021`. Живая официальная Playlist и Series News подтверждают прежний активный сезон: Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**. Состав прежний: 14 карточек, один Daily из 7 заданий, 53 очка.
- Проверены все 16 обязательных источников и свежие публикации текущей недели. Новых подтверждённых исправлений условий, решений, машин, share codes или ошибок засчитывания не найдено. **Сводка актуальна — содержательных изменений не требуется.** Обновлена только оперативная подсказка Daily: утром 06.09 доступны задания 03–05.09, задание 06.09 откроется в 21:30.
- Визуалы всех 14 карточек сверены заново. 13 отдельных Spring-плиток ForzaLabs остаются точными для текущей недели и совпадают с локальными файлами. Отдельной игровой Daily-плитки по-прежнему нет; временный уникальный визуал сохраняет статус preliminary. Итоги: **confirmed=13, community=0, preliminary=1, missing=0**. **openItems=1** — точная игровая Daily-плитка.
- Недоступность отдельных источников явно зафиксирована ниже и не использовалась как разрешение переносить старые решения, коды или изображения.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | checked: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — прямой MediaWiki API HTTP 200; список серий проверен, активный сезон дополнительно подтверждён официальной Playlist. |
| fandom_current | checked: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — API HTTP 200, содержимое Spring и Series 4 доступно; точной Daily-плитки нет. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — таблица Spring содержит текущие 14 активностей; верхний заголовок всё ещё Winter, но текст страницы прямо указывает Spring с 03.09. |
| forza_news | checked: [Series 4](https://forza.net/news/forza-horizon-6-series-4) — окно Spring 03–10.09 и сезонные награды подтверждены; следующая Series ещё не активна. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — раздел не прочитан web-reader; нового подтверждённого Spring-патча не найдено. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — публичная страница доступна; новых публичных ограничений Spring не найдено. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — редирект на страницу закрытия форума; текущенедельного официального треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) — текущенедельная разбивка и обсуждения проверены; новых исправлений не появилось. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — условия, карты и обсуждения проверены; отдельной Daily-плитки нет. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — дедлайн 10.09 14:30 UTC и 53 очка подтверждены; новых исправлений нет. |
| reddit_forzatune | unavailable: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — live `new.json` вернул HTTP 403; адресный поиск не дал проверяемого свежего Spring-поста. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — сайт доступен, недельный блок не соответствует текущей Series 4 Spring и не использован. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — каталог доступен; отдельной Collectibles-активности в Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — карта и текущая Spring-страница доступны; 13 точных плиток подтверждены, Daily-плитка отсутствует. |
| escorenews_fh6 | checked: [Spring guide](https://escorenews.com/en/article/80890-spring-series-4-weekly-festival-playlist-guide-in-forza-horizon-6-best-tunes-to-complete-challenges-in-fh6) — свежая статья текущей недели остаётся в поисковом индексе и подтверждает опубликованные решения; прямой серверный запрос вернул 403. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — оболочка HTTP 200, но читаемого подтверждённого списка свежих выпусков нет. |

# Source notes — 2026-09-05, Series 4 Spring

## Ежедневное уточнение — 2026-09-05, 06:01–06:08 +07:00

- RunId: `fh6-20260905-060139-164378`. Живая официальная таблица и Series News подтверждают прежний активный сезон: Series 4 «Horizon Mascot Party», Весна, до **10.09.2026 21:30 по Красноярску**. Состав прежний: 14 карточек, один Daily из 7 заданий, 53 очка.
- Проверены все 16 обязательных источников. Появились доступные независимые статьи Escorenews по Photo, Treasure и Spring в целом; они подтвердили уже опубликованные условия, точку сундука возле Delivery Job и ориентиры Edamame. В свежем обсуждении уточнено проблемное место Photo: снимок надёжнее делать под фиолетовым значком на мини-карте, между двумя группами фигур; если не засчиталось, помогает полный перезапуск игры. Это совет сообщества, в игре проектом не проверялся.
- Daily обновлён по текущей доступности: утром 05.09 открыты задания 03–04.09; задание 05.09 откроется в 21:30. Найден новый Spring tuning guide в r/forza / r/ForzaHorizon / r/ForzaHorizon6, но существующие коды уже имеют свежие подтверждения и не заменены без необходимости.
- Визуалы всех 14 карточек сверены заново. ForzaLabs по-прежнему показывает 13 отдельных точных Spring-плиток и не публикует отдельную Daily-плитку. Локальные файлы совпадают с проверенными карточками; итоги: **confirmed=13, community=0, preliminary=1, missing=0**. **openItems=1** — точная игровая Daily-плитка.
- Содержательное уточнение затронуло только инструкции Daily, Photo и Treasure и нижние ссылки источников; порядок, очки, машины, share codes, изображения и openItems не менялись. Старые сезоны, branding, support и analytics сохранены.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | checked: [категория](https://forza.fandom.com/wiki/Category:Series_(FH6)) — HTML/API web-reader нестабилен; прямой MediaWiki API HTTP 200, Series 1–4 и категория Series 5. |
| fandom_current | checked: [Spring](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — отдельная Spring_Season всё ещё `missingtitle`; API Series 4 revision 169617 подтверждает Spring и 53 очка. Точной Daily-плитки нет. |
| forza_playlist | checked: [живая Playlist](https://forza.net/fh6playlists) — таблица Spring содержит текущие 14 активностей; верхний заголовок всё ещё Winter, но строка 12 прямо направляет к Spring с 03.09. |
| forza_news | checked: [Series 4](https://forza.net/news/forza-horizon-6-series-4) — Spring-награды и окно 03–10.09 подтверждены; British Automotive заявлена следующей Series, не текущей сменой. |
| forza_support_release_notes | unavailable: [Release Notes](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — раздел и прямая статья 24.08 в web-reader недоступны; нового подтверждённого Spring-патча не заявлено. |
| forza_support_known_issues | checked: [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — публичная страница доступна и ведёт в закрытый Feedback Portal; новых публичных ограничений Spring не найдено. |
| forza_forums_official | no_current_item: [официальный форум](https://forums.forza.net/tag/official-info/1731) — редирект на страницу закрытия форума; текущенедельного треда нет. |
| reddit_forzahorizon | checked: [Spring breakdown](https://www.reddit.com/r/ForzaHorizon/comments/1w67gtq/fh6_series_4_spring_breakdown_and_rewards/) — перечень недели, Photo/Treasure и комментарии игроков о точной Photo-зоне проверены; новая tuning guide 04.09 также просмотрена. |
| reddit_forzahorizon6 | checked: [Spring guide](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — условия, карты и текущие обсуждения проверены; отдельной Daily-плитки не появилось. |
| reddit_forza | checked: [Information Thread](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — дедлайн 10.09 14:30 UTC и 53 очка подтверждены; найден свежий Spring Tuning Guide от 04.09. |
| reddit_forzatune | unavailable: [r/ForzaTune](https://www.reddit.com/r/ForzaTune/) — live `new.json` снова вернул HTTP 403; адресный поиск не дал проверяемого свежего Spring-поста. |
| forza_horizon_hub | no_current_item: [Hub](https://forzahorizonhub.com/) — сайт доступен, но недельный блок всё ещё не соответствует текущей Series 4 Spring; не использован. |
| forza_labs_collector | checked: [Collector Tool](https://forza.labsgg.com/collector-tool) — каталог доступен; отдельной Collectibles-активности в Spring нет. |
| forza_labs_map | checked: [Interactive Map](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) — карта доступна; Series Details остаётся на Spring 03.09 и содержит 13 точных игровых плиток, но не Daily. |
| escorenews_fh6 | checked: [Spring guide](https://escorenews.com/en/article/80890-spring-series-4-weekly-festival-playlist-guide-in-forza-horizon-6-best-tunes-to-complete-challenges-in-fh6), [Photo](https://escorenews.com/en/article/80887-peasinapod-photo-challenge-in-spring-series-4-of-forza-horizon-6-festival-playlist-where-is-edamame-area-at-the-mascot-party), [Treasure](https://escorenews.com/en/article/80888-tokyo-city-region-treasure-hunt-in-forza-horizon-6-spring-series-4-treasure-chest-location) — свежие статьи 03.09 доступны через поиск и подтверждают опубликованные решения. |
| dungg_playlist | unavailable: [плейлист DungG](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — оболочка HTTP 200, но читаемого списка свежих выпусков нет; адресный поиск не дал подтверждённого текущего выпуска. |

# Source notes — 2026-09-04, Series 4 Spring

## Ежедневное уточнение — 2026-09-04, 06:02–06:15 +07:00

- RunId: `fh6-20260904-060229-107804`. Активен прежний сезон: Series 4 «Horizon Mascot Party», Весна, 03.09–10.09.2026, смена в 21:30 по Красноярску. Проверены все 16 обязательных источников; ограничения доступа отдельно перечислены ниже.
- Состав: 14 карточек, один Daily из 7 заданий, 53 очка. В момент проверки открыт Daily 03.09; задание 04.09 откроется только в 21:30. Не создавался новый сезон по локальной дате.
- Устранены три пробела тюнинга: **2020 Toyota GR Supra — 584 324 652** (Ito Straight), **1991 Honda Beat — 867 935 515** (Seaside Trail), **1986 Audi #2 Audi Sport quattro S1 — 267 461 712** (Trial), все S1 800. Первый и второй — свежая подборка BigHedDjango, второй независимо повторён у ollumi, третий — текущенедельная competitive-подборка ollumi. Авторы сохраняются только в аудите; публично выводятся машины и коды. В игре рекомендации не тестировались.
- Конфликтующий 136 098 590 из первоначального гайда по-прежнему не используется. Существующие 140 205 851 и 947 984 645 заново сверены с гайдом Spring 03.09, не перенесены из Winter. Добавлены официальные награды, ориентиры Photo и разгон примерно 830 м с северо-востока для Ito.
- **Визуальный аудит каждой карточки:** 01 Cuti-e, 03 Photo, 04 Treasure, 05 Unlimited Buddies, 06 Hot Hatch Chasers, 07 Edamame Time Attack, 08 Ito Straight, 09 Seaside Trail, 10 Spring Cleaning, 11 Dragonborn, 12 Battle Royale, 13 Mini Games и 14 Edamame Circuit сверены по названию, машине/условию и награде с текущими плитками [ForzaLabs Spring](https://forza.labsgg.com/series/details). Все 13 скачаны заново в `tile-*.webp`, просмотрены контактным листом; исходное изображение целиком вписано в квадрат без обрезки текста. Размер каждого 36–81 КБ. Для 02 Daily отдельно проверены Fandom, Playlist и свежие Spring-гайды — точной плитки нет, текущий временный значок остаётся preliminary.
- Итог визуалов: **confirmed=13, community=0, preliminary=1, missing=0**. **openItems=1**: точная игровая Daily-плитка. Карты Photo/Treasure доступны в нижних ссылках; замена картинки Treasure на игровую плитку карту не удаляет. Архивы и постоянные branding/support/analytics сохранены.
- Обнаруженные ограничения: заголовок официальной Playlist ещё Winter, отдельная Fandom Spring отсутствует; ForzaTune JSON403, Escorenews и DungG не прочитаны полностью. Даты и условия Spring подтверждены доступными официальными таблицей/новостью и свежими независимыми публикациями. Недоступные страницы не заменялись старыми сведениями.

| Источник | Статус и результат текущей проверки |
|---|---|
| fandom_series_category | checked: [источник](https://forza.fandom.com/wiki/Category:Series_(FH6)) — MediaWiki API: Series 1–4 и категория Series 5; дату активного сезона определяет официальная таблица, не перечень категорий. |
| fandom_current | checked: [источник](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — API Spring_Season: missingtitle. API Series_4 revision 169617 подтверждает Spring 03–10.09 и 53 очка. Точной Daily-плитки нет. |
| forza_playlist | checked: [источник](https://forza.net/fh6playlists) — Таблица Spring подтверждает все 14 карточек, 7 Daily, пороги, маршруты и награды. Верхний заголовок ещё Winter; инструкция страницы прямо называет Spring с 03.09. |
| forza_news | checked: [источник](https://forza.net/news/forza-horizon-6-series-4) — News и Series 4 подтверждают Spring 03–10.09; новость Drift Attack от 26.08 анонсирует патч 07.09 и следующую Series 10.09, не текущую смену сезона. |
| forza_support_release_notes | checked: [источник](https://support.forza.net/hc/en-us/articles/54674846729875-FH6-Release-Notes-August-24-2026) — Раздел недоступен, прямая последняя связанная статья August 24 прочитана: Hotfix 1, исправления Road Discovery и vinyl; новых изменений Spring в ней нет. |
| forza_support_known_issues | checked: [источник](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — Доступна публичная страница с переходом на Feedback Portal; закрытый портал не проверен. Нового подтверждённого ограничения Spring нет. |
| forza_forums_official | no_current_item: [источник](https://forums.forza.net/tag/official-info/1731) — Редирект на forza.net/forums о закрытии старого форума; текущенедельного официального треда нет. |
| reddit_forzahorizon | checked: [источник](https://www.reddit.com/r/ForzaHorizon/comments/1w6am49/series_4_playlist_4_spring_competitive_tunes/) — Прочитаны свежие competitive tunes и breakdown 1w67gtq от 03.09. Trial Audi 267461712, Honda Beat 867935515; уточнены ориентиры фото. |
| reddit_forzahorizon6 | checked: [источник](https://www.reddit.com/r/ForzaHorizon6/comments/1w6hnou/series_04_week_4_spring_seasonal_tunes_mascot/) — Прочитаны Spring-гайды 1w6914y, 1w6hnou, 1w68z4z от 03.09. Supra 584324652 для Ito, Beat 867935515 для Seaside. Старый конфликт 136098590 исключён; карты и два прежних кода подтверждены свежим повторным чтением той же текущенедельной публикации. |
| reddit_forza | checked: [источник](https://www.reddit.com/r/forza/comments/1w6a0c8/fh6_spring_information_thread_series_4/) — Свежий Spring Information Thread от 03.09: конец 10.09 14:30 UTC, 53 очка; Total Rally включает разные эпохи. |
| reddit_forzatune | unavailable: [источник](https://www.reddit.com/r/ForzaTune/) — Лента web устарела, live new.json HTTP403; адресный поиск не дал проверяемой текущенедельной публикации. Отсутствие не объявляется исчерпывающим. |
| forza_horizon_hub | no_current_item: [источник](https://forzahorizonhub.com/) — Сайт доступен, weekly-блок всё ещё Series 1; текущего Spring-материала не найдено. |
| forza_labs_collector | checked: [источник](https://forza.labsgg.com/collector-tool) — Каталог автомобилей доступен. В текущей официальной Playlist отдельного Collectibles нет, карточка не добавляется искусственно. |
| forza_labs_map | checked: [источник](https://forza.labsgg.com/interactive-map) — Карта доступна. Дополнительно /series/details уже показывает активный Spring 03.09: скачаны и просмотрены 13 отдельных точных игровых плиток; Daily отсутствует. |
| escorenews_fh6 | unavailable: [источник](https://escorenews.com/en/games/forza-horizon-6) — Категория и тело свежей статьи 80888 Tokyo City Region недоступны. Поиск нашёл текущую статью, но недоступное содержимое не использовано как доказательство решения. |
| dungg_playlist | unavailable: [источник](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — Web throttled; HTTP200 оболочки при прямом запросе не даёт читаемый перечень видео. Адресный поиск не дал подтверждённого свежего выпуска; старые видео не переносились. |

## Внеплановый rollover — 2026-09-03, после 21:30 +07:00

- Технический повтор того же свежего аудита: `fh6-20260903-215325-279505`. Первая попытка `fh6-20260903-213252-423237` остановлена безопасно до публикации: локальные ссылки карт заменены на публичные HTTPS-ссылки. Контрольная сборка после исправления: validation/package passed, HTML 41 718 байт. Дополнительно исправлено сравнение времени HA receipt: граница проверки берётся с часов HA, а не Windows (наблюдалось расхождение около 1,2 секунды). Настройки/доступы HA не ослаблялись; настоящий receipt первой попытки подтверждён, пять сценариев watchdog прошли. Уведомление первой попытки не пересылалось; новый итог относится к отдельной восстановленной попытке. Все 16 проверок источников остаются свежими, в пределах одного внепланового обновления.
- RunId: `fh6-20260903-213252-423237`. Начало в 21:32; сбор свидетельств 21:32–21:50. Новый сезон подтверждён совместно официальной таблицей Spring, официальной новостью Series 4 и опубликованным после сброса Spring-гайдом. Верхняя плашка forza.net и ForzaLabs ещё отстают; это явно учтено, а не скрыто.
- Series 4 «Horizon Mascot Party», Весна: **03.09.2026 21:30 — 10.09.2026 21:30, Красноярск**. 14 карточек по фактическому составу недели, один Daily из 7 дней. Сумма очков: 5 + 7 + 2 + 3 + 5 + 5 + 3 + 2 + 2 + 10 + 3 + 2 + 3 + 1 = **53**. Monthly даёт 4 на Series, то есть 1 на сезон; повторное прохождение ранее закрытого Monthly не нужно. На старте открыт Daily 03.09; остальные открываются по датам 04–09.09, будущие задания не выдаются за доступные.
- Добавлены главы Cuti-e, маршруты, ограничения, точные пороги, карта Edamame и карта Tokyo City Treasure. Свежие тюнинги: 2020 Jimco #179 Hammerhead Class 1 — 140 205 851; 2013 Mercedes-Benz A 45 AMG — 947 984 645 для Hot Hatch Chasers и Edamame. Это советы сообщества, не тест в игре.
- **Конфликт тюнинга:** в одном новом гайде 136 098 590 указан и для 2002 Nissan Silvia Spec-R (оба PR Stunts), и для 1986 Audi #2 Audi Sport quattro S1 (Trial). Код исключён из всех трёх публичных карточек; рекомендации автомобилей оставлены как предварительные, 3 vehicleTune openItems.
- В официальной текстовой таблице и Series News второй Spring-приз — 1968 Dodge Dart HEMI Super Stock; Spring-инфографика по-прежнему рисует 1987 Nissan Be-1. Для отсутствующих картинок используется только вырезанный верхний сезонный баннер обзора; спорная часть с призами не выводится в карточках и не переносится в текст.
- Визуалы всех 14 активностей проверены: **confirmed=0, community=8, preliminary=6, missing=0**. Точные изображения Photo, двух чемпионатов, Time Attack, Speed Trap, Drift Zone, Trial взяты из свежего Spring-гайда; Treasure — отдельная карта текущей недели. Weekly временно использует изображение нужной Honda e из текущего Hot Hatch Chasers; Daily — значок Party Time из того же гайда. Для Dragonborn, Eliminator, Mini Games и Monthly отдельные текущие плитки не найдены, оставлен общий Spring fallback. Все 6 временных визуалов открыты в missingFields/openItems. Старые Winter-изображения и тюнинги не переносились.
- Карта фото: [Minamino / Edamame](https://preview.redd.it/fh6-series-4-spring-festival-playlist-guide-recommended-v0-7db3z2ugebnh1.png?width=1080&crop=smart&auto=webp&s=05adaa4c6fb50b42ceb68f1e56c6be7dded96db0). Карта сокровища: [Tokyo City, точка сундука](https://i.postimg.cc/SKvqZtxx/tes.png). Обе просмотрены; карты сохранены локально, карточные изображения перекодированы в компактный WebP без изменения содержания.
- **openItems=9:** 6 визуалов + 3 конфликтующих назначения кода. Неподтверждённые share codes отсутствуют. Старый JSON и Markdown сохраняются в архиве; постоянные project branding/support/analytics не изменяются.

| Источник | Статус и результат именно этого запуска |
|---|---|
| fandom_series_category | checked: [источник](https://forza.fandom.com/wiki/Category:Series_(FH6)) — MediaWiki API доступен: перечислены Series 1–4 и категория Series 5. Новый сезон определён не по категории, а по официальной Spring-таблице и свежему гайду. |
| fandom_current | checked: [источник](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Spring_Season) — Spring_Season возвращает missingtitle через API. Страница Series 4 (revision 169617) подтверждает период и 53 очка Spring; отдельные плитки пока получены из свежего Reddit. Общие иконки заново скачаны по текущему imageinfo API. |
| forza_playlist | checked: [источник](https://forza.net/fh6playlists) — После сброса таблица S04 Horizon Mascot Party - Spring содержит Cuti-e и все задания 03–10.09; ссылка на Spring-инфографику доступна. Верхний заголовок ещё Winter 27.08–03.09 — зафиксирована задержка обновления. Инфографика показывает иной второй приз, чем текстовая таблица/Series News; изображение общего обзора используется лишь временно и с оговоркой ниже. |
| forza_news | checked: [источник](https://forza.net/news/forza-horizon-6-series-4) — Официальная Series 4 действует 13.08–10.09; Spring-награды отнесены к 03–10.09. News проверен; новая серия из календарной догадки не создавалась. |
| forza_support_release_notes | unavailable: [источник](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) — Раздел и прямая статья Release Notes August 24 (54674846729875) в этом запуске недоступны. Предыдущие чтения не считаются новым аудитом содержимого. |
| forza_support_known_issues | checked: [источник](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) — Страница доступна; отдельных новых ограничений Spring не найдено. Feedback Portal за авторизацией не проверен. |
| forza_forums_official | no_current_item: [источник](https://forums.forza.net/tag/official-info/1731) — Перенаправляет на forza.net/forums — закрытие старого форума. Свежего текущенедельного треда на этой площадке нет. |
| reddit_forzahorizon | no_current_item: [источник](https://www.reddit.com/r/ForzaHorizon/) — Проверены лента и адресный поиск Series 4 Spring September 3 2026. Свежего FH6 Spring-гайда в этом subreddit не найдено; выдача содержит Winter и старый FH5. Прямой new.json вернул 403, ограничение отмечено. |
| reddit_forzahorizon6 | checked: [источник](https://www.reddit.com/r/ForzaHorizon6/comments/1w6914y/fh6_series_4_spring_festival_playlist_guide/) — Свежий гайд MarkCask4773 от 03.09 появился после начала запуска. Прочитан через web и авторизованный браузер: Spring 03–10.09 14:30 UTC, семь Daily, карты, три применённых назначения двух кодов. 13 файлов изображений выгружены из текущей страницы; используются только относящиеся к активностям. Код 136 098 590 конфликтует между Silvia и Audi и не опубликован. |
| reddit_forza | no_current_item: [источник](https://www.reddit.com/r/forza/) — Лента и поиск FH6 September 3 / Series 4 Spring проверены; актуальный Spring Information Thread не найден. Старый FH5 исключён; new.json 403. |
| reddit_forzatune | no_current_item: [источник](https://www.reddit.com/r/ForzaTune/) — Лента и поиск FH6 Series 4 Spring проверены; свежего подходящего тюнинга не найдено. Прямой JSON недоступен (403); коды с прошлой недели не переносились. |
| forza_horizon_hub | no_current_item: [источник](https://forzahorizonhub.com/) — Сайт доступен, свежего материала Spring 03–10.09 не обнаружено. Старый блок плейлиста не использован. |
| forza_labs_collector | checked: [источник](https://forza.labsgg.com/collector-tool) — Collector Tool доступен и представляет каталог автомобилей. Отдельной активности Collectibles в официальной Spring-таблице нет; не добавлялась искусственно. |
| forza_labs_map | checked: [источник](https://forza.labsgg.com/interactive-map) — Интерактивная карта доступна. Дополнительно /series/details ещё показывает Winter; Spring Sep 3 в навигации помечена future/locked. Это задержка этого агрегатора, не основание переносить Winter-карточки. |
| escorenews_fh6 | unavailable: [источник](https://escorenews.com/en/games/forza-horizon-6) — Категория недоступна; адресный поиск не дал свежего гайда Series 4 Spring. Старые статьи не использованы. |
| dungg_playlist | unavailable: [источник](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) — Плейлист не удалось прочитать. Адресный поиск DungG FH6 September 3 Spring не дал свежего подтверждённого выпуска; июльские видео исключены. |

## Совместимый сборщик и полный повторный аудит — 2026-09-03 07:25 +07:00

- RunId: `fh6-20260903-070936-588374`. По разрешению пользователя введён поддерживаемый проектный сборщик `fh6-portable/1.0.0` вместо отсутствующего legacy-файла плагина. Проверяются artifact/state, HTML, локальные assets, состав/CRC/SHA ZIP и receipt. Это не исходный валидатор плагина. 18 изолированных тестов сборщика и 25 тестов guard прошли; на прежних входных данных HTML сохранён точно, без редизайна.
- Сводка актуальна — содержательных изменений не требуется. Официальная живая Playlist подтверждает Winter 27.08–03.09, а Spring опубликована заранее. Дедлайн 03.09.2026 21:30 Красноярск; 14 карточек, Daily из 7 заданий, 53 очка. Все семь Daily уже открыты. Новые коды или прошлые сезонные решения не переносились; советы сообщества в игре не тестировались. Расхождения веб-таблицы по Matsumi 70/75 mph и Treasure остаются документированными, данные карточек не меняются.
- Аудит каждого визуала: AutoZOOM, CultClassic, Ohtani, Micro Circuits, Modern Marvels, Edamame Time Attack, Shirakawa-go, Highland Road, Matsumi Curve, Vision Chaser, Drift Tandem, Mini Games и Edamame Circuit сопоставлены с текущими отдельными плитками ForzaLabs. Для Daily отдельно проверены Fandom (53 изображения, revision 170723), официальный сезон, Reddit и адресный поиск: точного нового кадра нет. Локальные SHA всех 14 файлов закреплены в audit.json. Итог: `confirmed=13`, `community=0`, `preliminary=1`, `missing=0`; `openItems=1` — точная Daily-плитка.

| Источник | Проверка этого запуска |
|---|---|
| fandom_series_category | [Категория FH6](https://forza.fandom.com/wiki/Category:Series_(FH6)): HTML недоступен, MediaWiki API доступен; страницы Series 1–4, категория Series 5. |
| fandom_current | [Winter](https://forza.fandom.com/wiki/Forza_Horizon_6/Series_4/Winter_Season): HTML недоступен, API revision 170723, 53 изображения; нового Daily нет. |
| forza_playlist | [Живая Playlist](https://forza.net/fh6playlists): активная Winter; заголовок 27 августа — 3 сентября, Spring как предстоящая. |
| forza_news | [Новости](https://forza.net/news), [Series 4](https://forza.net/news/forza-horizon-6-series-4), [Drift Attack](https://forza.net/news/forza-horizon-6-drift-attack): сентябрьские анонсы не меняют текущую неделю. |
| forza_support_release_notes | [Раздел](https://support.forza.net/hc/en-us/sections/360000121153-Release-Notes-and-Known-Issues) и [прямая статья 24.08](https://support.forza.net/hc/en-us/articles/54674846729875-FH6-Release-Notes-August-24-2026) в этой попытке недоступны; прежнее успешное чтение не выдано за новое. |
| forza_support_known_issues | [Known Issues](https://support.forza.net/hc/en-us/articles/51701860097811-Forza-Horizon-6-Known-Issues) доступна, новых условий текущей недели нет; Feedback Portal за авторизацией не проверен. |
| forza_forums_official | [Official-info](https://forums.forza.net/tag/official-info/1731) перенаправляет на страницу закрытых форумов; свежего треда нет. |
| reddit_forzahorizon | [Текущенедельный tuning guide](https://www.reddit.com/r/ForzaHorizon/comments/1w1q972/fh6_series_4_winter_tuning_guide/) доступен; альтернативы не требуют заменять подтверждённые рекомендации. |
| reddit_forzahorizon6 | [Winter guide](https://www.reddit.com/r/ForzaHorizon6/comments/1vzu6tb/fh6_series_4_winter_festival_playlist_guide/) и [Seasonal Tunes](https://www.reddit.com/r/ForzaHorizon6/comments/1vzvho1/seasonal_tunes_by_awes0me_beau/) доступны; текущие ограничения и коды подтверждаются. |
| reddit_forza | [Winter Information Thread](https://www.reddit.com/r/forza/comments/1vzy764/fh6_winter_information_thread_series_4/) подтверждает 53 очка, семь Daily и смену 03.09 14:30 UTC. |
| reddit_forzatune | [Лента](https://www.reddit.com/r/ForzaTune/new/) доступна в индексе, но снимок старый; адресный поиск текущей Winter не нашёл свежей подходящей публикации. Не использована для новых кодов. |
| forza_horizon_hub | [Hub](https://forzahorizonhub.com/) доступен; сезонный блок Series 1 непригоден как подтверждение текущей недели. |
| forza_labs_collector | [Collector Tool](https://forza.labsgg.com/collector-tool): веб-извлечение недоступно, прямой HTTP 200, каталог 628; нового материала для пробелов нет. |
| forza_labs_map | [Карта](https://forza.labsgg.com/interactive-map) и [Series Details](https://forza.labsgg.com/series/details) доступны; Winter и 13 отдельных плиток, без Daily. |
| escorenews_fh6 | Категория недоступна; [недельный гайд](https://escorenews.com/ru/article/80714-polnyj-gayd-na-ispytaniya-festivalya-v-zimniy-sezon-seriya-4-v-forza-horizon-6-luchshie-mashiny-i-tyuning) открыт; оснований менять карточки не установлено. |
| dungg_playlist | [Плейлист](https://www.youtube.com/playlist?list=PLul9IRbs_3JgHPHVWOokS7lj4WXzekhrF) недоступен; адресный поиск не подтвердил выпуск текущей недели. Старые видео не переносились. |

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

## Rollover — 2026-09-10 23:04 +07:00 — Series 5 British Automotive, Лето

- Живая официальная новость Series 5 и пользовательские игровые кадры подтверждают начало **British Automotive — Лето** 10.09.2026 в 21:30 Asia/Krasnoyarsk. Новый сезон заканчивается 17.09.2026 в 21:30 Asia/Krasnoyarsk.
- Пользователь передал пять неизменённых кадров меню Festival Playlist. Оригиналы сохранены в `reports/assets/series-05-summer/source-playlist-01.png` … `source-playlist-05.png`; из них без изменения содержимого вырезаны 14 точных игровых плиток. Общие и старые сезонные иллюстрации не используются.
- Визуальный аудит: **14 community / 0 confirmed / 0 preliminary / 0 missing**. `automation/audit_visual_evidence.ps1` вернул `VISUAL_QUEUE_STATUS=READY`: точные плитки у всех карточек есть. Иконки в публичном тексте берутся только из постоянной библиотеки и только для типов, различимых на игровой плитке.
- Подтверждённый порядок и видимые факты: Weekly «Экстремальный Rover»; один Daily из 7 дней; `#JaguarSnap`; Treasure Hunt «Регион Ито»; «Лето в деревне»; «Герои автокросса»; Drift Zone Симанояма; Speed Trap «Побережье»; Danger Sign «Запуск в Ирокаве»; Trailblazer «Спуск Кодати»; Seasonal Job «Доставка еды в Токио»; Trial «Море спринт-кроссов»; Stunt Party «Мини-игры»; Monthly Rivals «Спринт по Симанояме». В state задано 14 карточек и 7 Daily; отсутствующие лимиты, маршруты и свежие share codes остались в `openItems`.

### Аудит обязательных источников — 2026-09-10 23:04 +07:00

| Источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki — FH6 Series category | HTTP 403 для автоматического запроса; свежая сезонная подстраница не использовалась как доказательство. |
| Forza Wiki / Fandom | HTTP 403 для автоматического запроса; старые карточки и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; страница доступна. Новый экран Playlist подтверждён игровыми кадрами пользователя. |
| Official Forza News | HTTP 200; статья `forza-horizon-6-series-5` подтверждает British Automotive и старт Festival Playlist 10.09 в 14:30 UTC. |
| Forza Support — Release Notes | Прежняя ссылка вернула HTTP 404; конкретные факты карточек из неё не брались. |
| Forza Support — Known Issues | HTTP 200; нового подтверждённого недельного бага, меняющего карточки, не найдено. |
| Official Forza Forums | HTTP 200; отдельного свежего breakdown Summer в official-info не найдено. |
| Reddit r/ForzaHorizon | HTTP 200; свежий официальный репост British Automotive найден, но точных условий и тюнингов Summer в него не добавлено. |
| Reddit r/ForzaHorizon6 | HTTP 200; свежий репост Series 5 найден, полного недельного гайда с решениями нет. |
| Reddit r/forza | HTTP 200; свежий официальный репост British Automotive подтверждает обновление, но не заменяет плитки условий. |
| Reddit r/ForzaTune | HTTP 200; свежего Series 5 Summer tune-post не найдено, коды прошлой недели не переносились. |
| Forza Horizon Hub | HTTP 200; точного решения Photo/Treasure Summer пока не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения не обнаружено. |
| ForzaLabs Interactive Map | HTTP 200; проверена как альтернатива для будущей точки Treasure. |
| Escorenews FH6 | HTTP 403; свежий гайд Summer недоступен, сведения не заимствовались. |
| DungG Seasonal Playlist | HTTP 200; отдельный подтверждённый выпуск Summer на момент проверки не найден. |

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

## Ежедневный аудит — 2026-09-11 00:38 +07:00 — компактные ссылки

- Живая Festival Playlist и официальная новость Series 5 по-прежнему доступны и подтверждают активную неделю British Automotive — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk. Карточки и точные пользовательские плитки не менялись; `audit_visual_evidence.ps1` — `READY`.
- По просьбе пользователя повторяющаяся ссылка на Playlist удалена из всех карточек. Оставлены только две ссылки с практическим назначением: официальная новость British Automotive в Weekly и интерактивная карта ForzaLabs у Treasure Hunt. Остальные подписи источника не являются ссылками.

| Источник | Результат проверки текущей недели |
|---|---|
| Forza Wiki — FH6 Series category | Автоматический запрос по-прежнему получает 403; старые данные не использовались. |
| Forza Wiki / Fandom | Автоматический запрос по-прежнему получает 403; старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; текущий сезон доступен. |
| Official Forza News | HTTP 200; Series 5 British Automotive остаётся актуальной. |
| Forza Support — Release Notes | Прежняя настроенная ссылка вернула 404; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; изменений, влияющих на карточки недели, не найдено. |
| Official Forza Forums | HTTP 200; нового недельного breakdown не найдено. |
| Reddit r/ForzaHorizon | HTTP 200; точных новых решений или кодов не найдено. |
| Reddit r/ForzaHorizon6 | HTTP 200; точных новых решений или кодов не найдено. |
| Reddit r/forza | HTTP 200; проверен официальный репост Series 5. |
| Reddit r/ForzaTune | HTTP 200; свежего Summer tune-post нет; старые коды не переносились. |
| Forza Horizon Hub | HTTP 200; точной точки Photo/Treasure пока нет. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельное решение не найдено. |
| ForzaLabs Interactive Map | HTTP 200; сохранена единственная прикладная ссылка для Treasure Hunt. |
| Escorenews FH6 | HTTP 403; новый независимый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200; подтверждённого отдельного walkthrough Summer нет. |

## Ежедневный аудит — 2026-09-11 04:38 +07:00 — точные плитки и полный Daily

- `r/forza` Information Thread Series 5 и свежий Summer breakdown подтвердили весь список Daily: Drift Attack; звезда в Speed Zone; Dirt Race; 3 Great Wreckage; парковка на Car Meet; обгон ghost в Rivals; 3 Drift/E-Drift. Все семь пунктов заполнены как community-подтверждённые, без ожидания новых скриншотов.
- Горизонтальные плитки повторно вырезаны непосредственно из оригиналов 2559×1599 по их фактическим границам: удалены чёрные разделители и полоса соседнего блока, правые края с наградой и типовой иконкой сохранены. Визуальная контрольная сетка проверена локально; общие или прошлосезонные изображения не использовались.
- В публичных карточках и в Markdown более нет ссылок на `visual.sourceImage` или предоставленные скриншоты. Оригиналы остаются только локальным доказательством в state и assets; для посетителя остаются только ссылки из `sourceHtml`, когда они имеют прикладную ценность.

| Обязательный источник | Проверка 11.09.2026 04:47 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403; материал недоступен автоматически, старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403; материал недоступен автоматически, старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; активная Playlist доступна. |
| Official Forza News | HTTP 200; Series 5 British Automotive подтверждена. |
| Forza Support — Release Notes | HTTP 404 по настроенному URL; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; влияющих на текущие активности изменений не найдено. |
| Official Forza Forums | HTTP 200; нового недельного breakdown не найдено. |
| Reddit r/ForzaHorizon | HTTP 200; проверены текущие Summer breakdown и tune-тред. |
| Reddit r/ForzaHorizon6 | HTTP 200; проверен текущий Summer tune-кросспост. |
| Reddit r/forza | HTTP 200; Information Thread Series 5 подтвердил все 7 Daily. |
| Reddit r/ForzaTune | HTTP 200; свежего Summer-поста с подтверждёнными кодами не найдено. |
| Forza Horizon Hub | HTTP 200; точного текущего решения Photo/Treasure не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения не найдено. |
| ForzaLabs Interactive Map | HTTP 200; проверена для будущей точки Treasure. |
| Escorenews FH6 | HTTP 403; независимый свежий гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200; отдельного подтверждённого walkthrough Summer не найдено. |

Визуальный аудит: 14/14 activity проверены; 12 точных пользовательских плиток подготовлены из сохранённых оригиналов текущей недели, 2 карточки без плиток остаются в очереди evidence. Общие, прошлосезонные и AI-визуалы не применялись.

## Ежедневный аудит — 2026-09-11 06:02 +07:00 — сводка актуальна

- Сводка актуальна — содержательных изменений не требуется. Живая Playlist и официальные Series 5 материалы по-прежнему подтверждают British Automotive / Лето до 17.09.2026 21:30 Asia/Krasnoyarsk; полный список из 7 Daily остаётся подтверждённым текущенедельным Information Thread r/forza.
- `audit_visual_evidence.ps1`: `READY`; все 14 визуалов повторно проверены. Точные игровые плитки и их SHA не изменились, новые или более точные варианты не обнаружены.

| Обязательный источник | Проверка 11.09.2026 06:02 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403; старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403; старые визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; активный сезон подтверждён. |
| Official Forza News | HTTP 200; Series 5 остаётся актуальной. |
| Forza Support — Release Notes | HTTP 404 по настроенному URL; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; влияющих изменений не найдено. |
| Official Forza Forums | HTTP 200; нового недельного breakdown нет. |
| Reddit r/ForzaHorizon | HTTP 200; свежих точных изменений не найдено. |
| Reddit r/ForzaHorizon6 | HTTP 200; свежих точных изменений не найдено. |
| Reddit r/forza | HTTP 200; Information Thread Series 5 проверен. |
| Reddit r/ForzaTune | HTTP 200; свежих подтверждённых Summer-кодов нет. |
| Forza Horizon Hub | HTTP 200; точного нового Photo/Treasure решения нет. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения нет. |
| ForzaLabs Interactive Map | HTTP 200; проверена для будущей точки Treasure. |
| Escorenews FH6 | HTTP 403; свежий гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200; отдельного подтверждённого Summer walkthrough нет. |

## Уточнение ограничений и тюнингов — 2026-09-11 06:43 +07:00

- Свежий `FH6: Series 5 Summer Breakdown and Rewards` в r/ForzaHorizon дал полные ограничения, трассы и цели: Trial `A 700`, Total Buggies & Offroad; Rural Summer `A 700`, Retro Supercars; Cross Country Heroes `A 700`, Sports Utility Heroes; Drift Attack без ограничения с целью 60 000; PR Stunts `A 700` / `S1 800` / `B 600` для автомобилей United Kingdom.
- Свежий Series 5 Information Thread r/forza независимо подтвердил те же условия, 2025 McLaren W1 для Monthly Rivals, три доставки для Seasonal Job и расписание Horizon Stunt Party. Точные рекомендации и 9-значные коды взяты из свежего competitive-tunes треда r/ForzaHorizon; имена авторов не выводятся.
- Закрыты 28 устаревших пунктов: Weekly, Photo, оба Championship, Drift Attack, три PR Stunts, Seasonal Job, Trial, Stunt Party и Monthly Rivals. Открытым остаётся только местоположение сундука Treasure Hunt; без подтверждённой точки оно не выдумывается.
- Визуальный аудит: `READY`, 14/14 текущесезонных плиток без изменений; новых плиток не потребовалось.

| Обязательный источник | Проверка 11.09.2026 06:43 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403; старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403; старые визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; активная Playlist подтверждена. |
| Official Forza News | HTTP 200; Series 5 проверена. |
| Forza Support — Release Notes | HTTP 404 по настроенному URL; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; критичных изменений не найдено. |
| Official Forza Forums | HTTP 200; нового breakdown нет. |
| Reddit r/ForzaHorizon | HTTP 200; использованы свежие Summer breakdown и competitive tunes. |
| Reddit r/ForzaHorizon6 | HTTP 200; текущий tune-кросспост подтверждён. |
| Reddit r/forza | HTTP 200; Information Thread Series 5 использован для независимого подтверждения. |
| Reddit r/ForzaTune | HTTP 200; отдельного более свежего Summer-поста нет. |
| Forza Horizon Hub | HTTP 200; точной точки Treasure нет. |
| ForzaLabs Collector Tool | HTTP 200; точного Treasure-решения нет. |
| ForzaLabs Interactive Map | HTTP 200; проверена для будущей точки сундука. |
| Escorenews FH6 | HTTP 403; данные не заимствовались. |
| DungG Seasonal Playlist | HTTP 200; отдельного подтверждённого Summer walkthrough нет. |

## Ежедневный аудит — 2026-09-12 06:05 +07:00

- Активный сезон подтверждён по живой официальной Playlist: Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk.
- Свежий текущенедельный гайд r/ForzaHorizon6 подтвердил все Daily и дал машину с 9-значным share code для доступного 12.09 задания «Гонка по грунту»: 2018 Mercedes-Benz X-Class, `832 534 809`. Это добавлено в Daily; остальные факты и порядок карточек не изменились.
- Визуальный аудит: 14/14 activity проверены; 12 точных текущенедельных плиток и 2 корректно отсутствующих визуала без изменений. Новые, более точные либо прошлосезонные визуалы не применялись.

| Обязательный источник | Проверка 12.09.2026 06:05 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | Доступ автоматического клиента ограничен; старые данные не использовались. |
| Forza Wiki — текущий сезон | Доступ автоматического клиента ограничен; старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; Series 5 British Automotive — Summer подтверждён. |
| Official Forza News | HTTP 200; нового материала, меняющего неделю, не найдено. |
| Forza Support — Release Notes | Настроенная ссылка недоступна; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; влияющих на текущие активности изменений нет. |
| Official Forza Forums | HTTP 200; нового недельного breakdown нет. |
| Reddit r/ForzaHorizon | Проверен свежий Summer breakdown; условия недели подтверждены. |
| Reddit r/ForzaHorizon6 | Свежий текущенедельный гайд подтвердил Daily и дал код для Daily 12.09. |
| Reddit r/forza | Information Thread Series 5 подтверждает активный сезон, полный Daily и ограничения. |
| Reddit r/ForzaTune | Свежего подтверждённого Summer-поста не найдено; старые коды не переносились. |
| Forza Horizon Hub | HTTP 200; точного решения Treasure Hunt не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения Treasure Hunt не найдено. |
| ForzaLabs Interactive Map | HTTP 200; проверена для будущей точки сундука. |
| Escorenews FH6 | Доступ автоматического клиента ограничен; новые данные не использовались. |
| DungG Seasonal Playlist | Автоматическая проверка недоступна; отдельного нового walkthrough не подтверждено. |

## Ежедневный аудит — 2026-09-13 06:03 +07:00 — сводка актуальна

- Сводка актуальна — содержательных изменений не требуется. Живая официальная Playlist подтверждает Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk. Полный список из 7 Daily и единственная открытая точка Treasure Hunt не получили новых подтверждённых изменений.
- Визуальный аудит: 14/14 activity проверены; подготовленные точные текущесезонные плитки без изменений, `audit_visual_evidence.ps1` вернул `READY`. Общие, прошлосезонные и AI-визуалы не применялись.

| Обязательный источник | Проверка 13.09.2026 06:03 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403; материал недоступен автоматическому клиенту, старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403; старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; British Automotive Summer (10–17 сентября) подтверждён. |
| Official Forza News | HTTP 200; нового материала, меняющего текущую неделю, не найдено. |
| Forza Support — Release Notes | Настроенная ссылка вернула HTTP 404; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; новых проблем, влияющих на текущие активности, не найдено. |
| Official Forza Forums | HTTP 200; официальный форум закрыт, нового недельного breakdown нет. |
| Reddit r/ForzaHorizon | HTTP 403 для JSON; текущенедельный поиск не дал нового подтверждённого решения или кода. |
| Reddit r/ForzaHorizon6 | HTTP 403 для JSON; нового подтверждённого Summer-материала не найдено. |
| Reddit r/forza | HTTP 403 для JSON; нового Information Thread или уточнения активностей не найдено. |
| Reddit r/ForzaTune | HTTP 403 для JSON; свежего подтверждённого Summer tune-post нет. |
| Forza Horizon Hub | HTTP 200; точного нового решения Photo/Treasure не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения Treasure Hunt не найдено. |
| ForzaLabs Interactive Map | HTTP 200; проверена для точки сундука, точка не подтверждена. |
| Escorenews FH6 | HTTP 403; свежий независимый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200, но показана cookie-страница YouTube; новый walkthrough не подтверждён. |

## Ежедневный аудит — 2026-09-17 06:02 +07:00 — сводка актуальна

- Живая официальная Playlist по-прежнему показывает Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk. На странице уже виден будущий Autumn как следующий сезон, но фактической смены до дедлайна нет; rollover не запускается.
- Текущие Daily, ограничения, тюнинги и закрытый 16.09 Treasure Hunt не изменились. `openItems=0`; содержательных изменений в карточках не найдено.
- Визуальный аудит: 14/14 activity проверены; `audit_visual_evidence.ps1` вернул `READY`. Точные подготовленные плитки текущего сезона и их SHA не изменились, общие/прошлосезонные/AI-визуалы не применялись.

| Обязательный источник | Проверка 17.09.2026 06:02 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403; старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403; старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; Summer ещё активен до 21:30, Autumn отмечен как следующий сезон. |
| Official Forza News | HTTP 200; Series 5 подтверждена, нового изменения текущей недели нет. |
| Forza Support — Release Notes | HTTP 403; отдельный новый факт не использован. |
| Forza Support — Known Issues | HTTP 403; влияющих изменений не подтверждено. |
| Official Forza Forums | HTTP 200; нового официального breakdown нет. |
| Reddit r/ForzaHorizon | HTTP 200; нового подтверждённого изменения Summer не найдено. |
| Reddit r/ForzaHorizon6 | HTTP 200; Daily и текущие рекомендации совпадают со state. |
| Reddit r/forza | HTTP 200; Information Thread Series 5 подтверждает дедлайн 17.09 14:30 UTC. |
| Reddit r/ForzaTune | HTTP 200; нового подтверждённого Summer tune-поста нет. |
| Forza Horizon Hub | HTTP 200; нового материала текущей недели нет. |
| ForzaLabs Collector Tool | HTTP 200; новых решений нет. |
| ForzaLabs Interactive Map | HTTP 200; закрытый маршрут Treasure Hunt не требует уточнения. |
| Escorenews FH6 | HTTP 403; новый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200, cookie-страница; нового Summer walkthrough не подтверждено. |

## Ежедневный аудит — 2026-09-16 06:04 +07:00

- Живая официальная Playlist подтверждает активный Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk; перехода сезона нет. Полный список из 7 Daily, игровые ограничения и награды совпадают с текущей сводкой.
- Найдено и проверено новое текущее решение единственного открытого пункта: сундук Treasure Hunt «Регион Ито» находится к югу от аэродрома Ито, перед железнодорожным переездом между северной и южной частями полей. У дома справа нужно повернуть налево, не доезжая переезда, в маленький участок без деревьев. Решение подтверждено свежей статьёй PC Gamer от 10.09 и закрывает `openItems`.
- Визуальный аудит: 14/14 activity проверены; `audit_visual_evidence.ps1` вернул `READY`. Точные подготовленные плитки текущего сезона и их SHA не изменились; общие, прошлосезонные и AI-визуалы не применялись.

| Обязательный источник | Проверка 16.09.2026 06:04 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403 (Cloudflare); старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403 (Cloudflare); старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; British Automotive Summer подтверждён до 17.09, включая все 7 Daily, ограничения и награды. |
| Official Forza News | HTTP 200; British Automotive Series 5 остаётся актуальной, нового недельного материала нет. |
| Forza Support — Release Notes | Настроенная ссылка вернула HTTP 404; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; новых проблем, влияющих на активности недели, не найдено. |
| Official Forza Forums | HTTP 200; нового официального недельного breakdown нет. |
| Reddit r/ForzaHorizon | HTTP 200; проверен текущенедельный British Automotive материал, новых противоречащих фактов нет. |
| Reddit r/ForzaHorizon6 | HTTP 200; подтверждён полный список Daily и актуальные рекомендации, нового точного факта поверх state нет. |
| Reddit r/forza | HTTP 200; Information Thread Series 5 подтверждает сезон, дедлайн, Treasure clue и ограничения. |
| Reddit r/ForzaTune | HTTP 200; свежего подтверждённого Summer-кода нет. |
| Forza Horizon Hub | HTTP 200; нового более точного Photo/Treasure материала не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного более точного Treasure-решения нет. |
| ForzaLabs Interactive Map | HTTP 200; проверена для точки сундука; точнее опубликованного маршрута не даёт. |
| Escorenews FH6 | HTTP 403; свежий независимый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200, но показана cookie-страница YouTube; отдельный новый Summer walkthrough не подтверждён. |

## Ежедневный аудит — 2026-09-14 06:05 +07:00

- Живая официальная Playlist и официальная новость по-прежнему подтверждают Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk. Перехода сезона нет.
- Свежий текущенедельный пост r/ForzaHorizon6 `British Automotive Summer Cars and Tune Codes` подтвердил рекомендации и 9-значные коды для всех семи Daily. В карточку Daily добавлены: 1992 Mazda RX-7 Type R `182 459 719` для Drift Attack / Drift Skills, 2021 Pagani Huayra R `182 399 645` для Speed Zone и 2018 Mercedes-Benz X-Class `832 534 809` для Dirt Race, Great Wreckage, Car Meet и Rivals. Имена авторов не выводятся.
- Пост о сундуке Treasure Hunt найден, но доступная текстовая часть не содержит точной проверяемой точки/координат; она не перенесена в сводку. `openItems` для сундука остаётся честно открытым.
- Визуальный аудит: 14/14 activity проверены; подготовленные точные плитки текущего сезона и их SHA не изменились, `audit_visual_evidence.ps1` вернул `READY`. Общие, прошлосезонные и AI-визуалы не применялись.

| Обязательный источник | Проверка 14.09.2026 06:05 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403 (Cloudflare); старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403 (Cloudflare); старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; `British Automotive - Summer` остаётся текущей Playlist и подтверждает порядок/ограничения. |
| Official Forza News | HTTP 200; Series 5 British Automotive подтверждена, более нового материала для активной недели нет. |
| Forza Support — Release Notes | Настроенная ссылка вернула HTTP 404; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; новых проблем, влияющих на активности недели, не найдено. |
| Official Forza Forums | HTTP 200; официальный форум закрыт, нового недельного breakdown нет. |
| Reddit r/ForzaHorizon | Проверен свежий пост/репост British Automotive; новых противоречащих условий или кодов нет. |
| Reddit r/ForzaHorizon6 | Свежий Summer Cars and Tune Codes использован для полного набора Daily; отдельный пост о сундуке не дал текстовой точной координаты. |
| Reddit r/forza | Свежий Information Thread Series 5 подтверждает активную неделю, её дедлайн и полный список Daily. |
| Reddit r/ForzaTune | Свежего подтверждённого Summer-поста не найдено; старые коды не переносились. |
| Forza Horizon Hub | HTTP 200; точного нового решения Treasure Hunt не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения Treasure Hunt не найдено. |
| ForzaLabs Interactive Map | HTTP 200; проверена для точки сундука, точка не подтверждена. |
| Escorenews FH6 | HTTP 403 (Cloudflare); новый независимый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200, но показана cookie-страница YouTube; новый walkthrough не подтверждён. |

## Ежедневный аудит — 2026-09-15 06:03 +07:00 — сводка актуальна

- Сводка актуальна — содержательных изменений не требуется. Живая официальная Playlist подтверждает Series 5 «British Automotive» — Лето до 17.09.2026 21:30 Asia/Krasnoyarsk, включая порядок всех семи Daily, текущие ограничения и награды. Перехода сезона нет.
- Проверены свежие текущенедельные материалы Reddit: новых подтверждённых ограничений, решений Treasure Hunt, машин или 9-значных кодов поверх опубликованного полного набора Daily не найдено. Точная точка сундука по-прежнему не подтверждена и остаётся единственным открытым пунктом.
- Визуальный аудит: 14/14 activity проверены; подготовленные точные плитки активного сезона и их SHA не изменились, `audit_visual_evidence.ps1` вернул `READY`. Общие, прошлосезонные и AI-визуалы не применялись.

| Обязательный источник | Проверка 15.09.2026 06:03 +07:00 |
|---|---|
| Forza Wiki — Series (FH6) | HTTP 403 (Cloudflare); старые данные не использовались. |
| Forza Wiki — текущий сезон | HTTP 403 (Cloudflare); старые данные и визуалы не переносились. |
| Official Forza Festival Playlist | HTTP 200; British Automotive Summer активен до 17.09, порядок и ограничения подтверждены. |
| Official Forza News | HTTP 200; нового материала, меняющего активную неделю, не найдено. |
| Forza Support — Release Notes | Настроенная ссылка вернула HTTP 404; факты карточек не брались. |
| Forza Support — Known Issues | HTTP 200; новых проблем, влияющих на активности недели, не найдено. |
| Official Forza Forums | HTTP 200; официальный форум закрыт, нового недельного breakdown нет. |
| Reddit r/ForzaHorizon | Проверен текущенедельный British Automotive материал; нового подтверждённого факта нет. |
| Reddit r/ForzaHorizon6 | Проверены актуальные Summer обсуждения и Daily-коды; нового подтверждённого изменения нет. |
| Reddit r/forza | Information Thread Series 5 проверен: сезон, дедлайн и полный Daily совпадают со state. |
| Reddit r/ForzaTune | Свежего подтверждённого Summer-поста не найдено; старые коды не переносились. |
| Forza Horizon Hub | HTTP 200; точного нового решения Treasure Hunt не найдено. |
| ForzaLabs Collector Tool | HTTP 200; текущенедельного решения Treasure Hunt не найдено. |
| ForzaLabs Interactive Map | HTTP 200; проверена для точки сундука, точка не подтверждена. |
| Escorenews FH6 | HTTP 403 (Cloudflare); новый независимый гайд недоступен. |
| DungG Seasonal Playlist | HTTP 200, но показана cookie-страница YouTube; новый walkthrough не подтверждён. |

## Автоматический аудит — 2026-09-17T22:43:41+07:00 — deterministic service

- Активный сезон подтверждён по официальной Playlist: Forza Horizon 6: Как пройти Series 5 «British Automotive» — Лето до 2026-09-17T21:30:00+07:00.
- Сервис проверил все 16 обязательных источника и 14 визуалов; содержательные карточки не изменялись автоматически.
- Неоднозначные новые факты не переносились: для них создаётся отдельный candidate-файл, а не изменение state.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: HTTP 403; no stale data reused. |
| `fandom_current` | unavailable: HTTP 403; no stale data reused. |
| `forza_playlist` | checked: HTTP 200; active British Automotive Summer confirmed from official Playlist. |
| `forza_news` | no_current_item: HTTP 200; no deterministic current-week delta detected. |
| `forza_support_release_notes` | unavailable: HTTP 404; no stale data reused. |
| `forza_support_known_issues` | unavailable: HTTP 403; no stale data reused. |
| `forza_forums_official` | no_current_item: HTTP 200; no deterministic current-week delta detected. |
| `reddit_forzahorizon` | unavailable: HTTP 403; no stale data reused. |
| `reddit_forzahorizon6` | unavailable: HTTP 403; no stale data reused. |
| `reddit_forza` | unavailable: HTTP 403; no stale data reused. |
| `reddit_forzatune` | unavailable: HTTP 403; no stale data reused. |
| `forza_horizon_hub` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_collector` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_map` | unavailable: HTTP network error; no stale data reused. |
| `escorenews_fh6` | unavailable: HTTP 403; no stale data reused. |
| `dungg_playlist` | unavailable: HTTP 200 cookie/consent page; no walkthrough inferred. |

## 2026-09-17T22:51:35+07:00 — Series 5 Autumn rollover audit

Живой переход подтверждён официальной Playlist и свежими текущенедельными Information Thread/гайдами Reddit: Series 5 British Automotive, Autumn, 17–24 сентября 2026, дедлайн 2026-09-24 21:30 Asia/Krasnoyarsk. Все 16 обязательных источников проверены; Forza Playlist и Reddit-публикации дали условия, награды, ограничения классов и актуальные share codes. Fandom/Support/часть вспомогательных источников недоступны или не содержат текущего материала — старые решения и изображения не переносились.

| Источник | Результат текущего аудита |
|---|---|
| fandom_series_category | unavailable: HTTP 403; Autumn подтверждён официальными и Reddit-источниками. |
| fandom_current | unavailable: HTTP 403; точные Autumn-плитки не найдены. |
| forza_playlist | checked: HTTP 200; Series 5 Autumn и порядок активностей подтверждены. |
| forza_news | no_current_item: HTTP 200; отдельной Autumn-статьи не найдено. |
| forza_support_release_notes | unavailable: HTTP 403. |
| forza_support_known_issues | unavailable: HTTP 403. |
| forza_forums_official | no_current_item: HTTP 200; свежего Autumn-подтверждения нет. |
| reddit_forzahorizon | checked: свежий Autumn breakdown с маршрутами и ограничениями. |
| reddit_forzahorizon6 | checked: свежий Autumn guide с тюнингами и 9-значными кодами. |
| reddit_forza | checked: свежая Autumn Information Thread с полным списком активностей. |
| reddit_forzatune | no_current_item: отдельного свежего поста не найдено; тюнинги взяты из FH6 guide. |
| forza_horizon_hub | unavailable: сеть/страница недоступна. |
| forza_labs_collector | unavailable: сеть/страница недоступна. |
| forza_labs_map | unavailable: сеть/страница недоступна. |
| escorenews_fh6 | unavailable: HTTP 403. |
| dungg_playlist | unavailable: cookie/consent page; видео-решения не выводились. |

Проверка визуалов: 14/14 статусов `missing`. Точные игровые плитки Autumn не найдены в доступных источниках; старые Summer-визуалы не переиспользованы. `automation/audit_visual_evidence.ps1` сформировал очередь необрезанных пользовательских скриншотов для всех activity. После получения скриншотов будут сохранены оригиналы и вырезаны только точные границы плиток.

## 2026-09-18 — пользовательские Autumn-плитки

Из пяти присланных скриншотов сохранены оригиналы в `reports/assets/series-05-autumn/evidence/` и вырезаны точные границы плиток без наложений для Weekly, Photo, Collectibles, Offroad Scramble, Toys On The Road, Lakeside Valley Speed Trap, Inner City Run Drift Zone, Ocean Highway Speed Zone, Trial, Horizon Drift, Horizon Stunt Party и Hide & Seek. Monthly Rivals добавлен из прошлой недели по прямому указанию пользователя. Daily не добавлялся: исходный кадр обрезан снизу и не показывает полную плитку; оставлен в openItems/missingFields.

## 2026-09-18 — дополнительный поиск Autumn-плиток

Проверены свежие гайды r/ForzaHorizon6, официальный `forza.net/fh6playlists`, PandaPlay и поиск изображений. Найдены car renders и сезонные/общие скриншоты, но не отдельные полные игровые плитки 14 активностей. Эти изображения не подключались: они не соответствуют требованию точной плитки и могут содержать обрезку или другой формат. Очередь пользовательских необрезанных скриншотов остаётся актуальной.

## Автоматический аудит — 2026-09-17T22:45:19+07:00 — deterministic service

- Активный сезон подтверждён по официальной Playlist: Forza Horizon 6: Как пройти Series 5 «British Automotive» — Лето до 2026-09-17T21:30:00+07:00.
- Сервис проверил все 16 обязательных источника и 14 визуалов; содержательные карточки не изменялись автоматически.
- Неоднозначные новые факты не переносились: для них создаётся отдельный candidate-файл, а не изменение state.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: HTTP 403; no stale data reused. |
| `fandom_current` | unavailable: HTTP 403; no stale data reused. |
| `forza_playlist` | checked: HTTP 200; active British Automotive Summer confirmed from official Playlist. |
| `forza_news` | no_current_item: HTTP 200; no deterministic current-week delta detected. |
| `forza_support_release_notes` | unavailable: HTTP 403; no stale data reused. |
| `forza_support_known_issues` | unavailable: HTTP 403; no stale data reused. |
| `forza_forums_official` | no_current_item: HTTP 200; no deterministic current-week delta detected. |
| `reddit_forzahorizon` | no_current_item: HTTP 200; no current-week marker found; stale material not reused. |
| `reddit_forzahorizon6` | no_current_item: HTTP 200; no current-week marker found; stale material not reused. |
| `reddit_forza` | no_current_item: HTTP 200; no current-week marker found; stale material not reused. |
| `reddit_forzatune` | no_current_item: HTTP 200; no current-week marker found; stale material not reused. |
| `forza_horizon_hub` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_collector` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_map` | unavailable: HTTP network error; no stale data reused. |
| `escorenews_fh6` | unavailable: HTTP 403; no stale data reused. |
| `dungg_playlist` | unavailable: HTTP 200 cookie/consent page; no walkthrough inferred. |
## 2026-09-18 — Autumn Series 5: пользовательские точные плитки

- Получены пять исходных игровых скриншотов пользователя; оригиналы сохранены в `reports/assets/series-05-autumn/evidence/`.
- Из них вырезаны точные плитки без наложений для Weekly, Photo, Collectibles, трёх Championship, трёх PR, Trial и трёх Horizon Play: 12 подготовленных визуалов (`horizontal`/`vertical` по исходной ориентации).
- Monthly Rivals восстановлена из сохранённой плитки прошлой недели по прямому указанию пользователя; исходник и подготовленный файл сохранены локально, перенос зафиксирован как исключение.
- Daily: присланный кадр показывает только часть списка и не содержит полной текущей плитки; визуал оставлен `missing`, добавлен в `openItems`/`missingFields`, запрос полного скриншота не закрыт.
- Визуальный аудит: `confirmed=0`, `community=13` (12 пользовательских Autumn-плиток и Monthly Rivals по явному исключению), `preliminary=0`, `missing=1` (Daily). Ссылки на скриншоты в карточки не добавлялись.

## 2026-09-19 — ежедневный guarded-аудит Series 5 Autumn

- Все 16 обязательных источников проверены и зарегистрированы в audit.json запуска `fh6-20260919-054003-329630`: `forza_playlist` подтвердил активную Autumn Series 5; недоступные/без свежего материала источники отмечены без переноса старых решений.
- Повторно проверены ссылки для активностей с конкретной локацией: Photo Challenge → Shirakawa-go (GismoLand), Collectibles/Tire Hunt → Shimanoyama (Escorenews). Ссылок на скриншоты нет.
- Визуальный аудит: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым списком без карточки-скриншота и без чипа «Плитка: нужен скриншот».
- Сводка актуальна — содержательных изменений не требуется.

## 2026-09-22 — ежедневный guarded-аудит Series 5 Autumn

- Все обязательные источники повторно проверены; живая Playlist подтверждает Autumn Series 5. Недоступные или без свежего текущенедельного материала источники отмечены без переноса устаревших данных.
- Визуальный аудит всех 14 активностей: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым блоком без скриншота и без публичного чипа «Плитка: нужен скриншот».
- Ссылки локаций Photo Challenge (Shirakawa-go) и Collectibles/Tire Hunt (Shimanoyama) сохранены; ссылок на скриншоты нет.
- Содержательных изменений карточек не найдено; обновляется служебное время полной проверки.

## 2026-09-24 — ежедневный guarded-аудит Series 5 Autumn

- Все обязательные источники повторно проверены; живая Playlist подтверждает Autumn Series 5. Недоступные или без свежего текущенедельного материала источники отмечены без переноса устаревших данных.
- Визуальный аудит всех 14 активностей: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым блоком без скриншота и без публичного чипа «Плитка: нужен скриншот».
- Ссылки локаций Photo Challenge (Shirakawa-go) и Collectibles/Tire Hunt (Shimanoyama) сохранены; ссылок на скриншоты нет.
- Содержательных изменений карточек не найдено; обновляется служебное время полной проверки.

## 2026-09-23 — ежедневный guarded-аудит Series 5 Autumn

- Все обязательные источники повторно проверены; живая Playlist подтверждает Autumn Series 5. Недоступные или без свежего текущенедельного материала источники отмечены без переноса устаревших данных.
- Визуальный аудит всех 14 активностей: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым блоком без скриншота и без публичного чипа «Плитка: нужен скриншот».
- Ссылки локаций Photo Challenge (Shirakawa-go) и Collectibles/Tire Hunt (Shimanoyama) сохранены; ссылок на скриншоты нет.
- Содержательных изменений карточек не найдено; обновляется служебное время полной проверки.

## 2026-09-20 — ежедневный guarded-аудит Series 5 Autumn

- Все обязательные источники повторно проверены; подтверждён прежний активный сезон Autumn Series 5, недоступные и без текущенедельного материала источники отмечены без переноса устаревших решений.
- Визуальный аудит всех 14 активностей: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым блоком без скриншота и без публичной отметки «Плитка: нужен скриншот».
- Проверены короткие ссылки для Photo Challenge (Shirakawa-go) и Collectibles/Tire Hunt (Shimanoyama); ссылки на скриншоты не используются.
- Содержательных изменений карточек не найдено; требуется обновить только служебное время проверки через полный конвейер.

## 2026-09-21 — ежедневный guarded-аудит Series 5 Autumn

- Все обязательные источники повторно проверены; живая Playlist подтверждает Autumn Series 5. Недоступные или без свежего материала источники зафиксированы без переноса устаревших решений.
- Визуальный аудит всех 14 активностей: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (Daily). Daily остаётся текстовым списком без скриншота и без публичной отметки «Плитка: нужен скриншот».
- Ссылки для Photo Challenge (Shirakawa-go) и Collectibles/Tire Hunt (Shimanoyama) сохранены; ссылок на скриншоты нет.
- Сводка актуальна — содержательных изменений не требуется.

## 2026-09-24T21:43:36+07:00 — Series 5 Winter rollover audit

- Официальная Playlist подтверждает Series 5 British Automotive — Winter: 24 сентября – 1 октября 2026.
- Новое состояние создано только из явных фактов официальной Playlist и новости Forza; неуточнённые условия и решения оставлены в openItems.
- Визуальный аудит: 14/14 точных Winter-плиток отсутствуют. Старые Autumn-визуалы не переиспользованы; очередь ожидает оригинальные полные скриншоты пользователя.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: HTTP 403; no stale data reused. |
| `fandom_current` | unavailable: HTTP 403; no stale data reused. |
| `forza_playlist` | checked: HTTP 200; active Series 5 British Automotive Winter confirmed by official Playlist. |
| `forza_news` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `forza_support_release_notes` | unavailable: HTTP 403; no stale data reused. |
| `forza_support_known_issues` | unavailable: HTTP 403; no stale data reused. |
| `forza_forums_official` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `reddit_forzahorizon` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `reddit_forzahorizon6` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `reddit_forza` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `reddit_forzatune` | no_current_item: HTTP 200; no deterministic current-week material found. |
| `forza_horizon_hub` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_collector` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_map` | unavailable: HTTP network error; no stale data reused. |
| `escorenews_fh6` | unavailable: HTTP 403; no stale data reused. |
| `dungg_playlist` | unavailable: HTTP 200 cookie/consent page; no walkthrough inferred. |

## 2026-09-24T22:35:17+07:00 — публикация ссылки Steam в веб-сводке

- Все обязательные источники перепроверены; активная Winter Series 5 подтверждена официальной Playlist. Карточки и игровые визуалы не менялись.
- В финальный блок после графика аудитории добавлена прямая ссылка на публичное руководство Steam.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: HTTP 403; no stale data reused. |
| `fandom_current` | unavailable: HTTP 403; no stale data reused. |
| `forza_playlist` | checked: HTTP 200; active Winter confirmed. |
| `forza_news` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `forza_support_release_notes` | unavailable: HTTP 403; no stale data reused. |
| `forza_support_known_issues` | unavailable: HTTP 403; no stale data reused. |
| `forza_forums_official` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `reddit_forzahorizon` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `reddit_forzahorizon6` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `reddit_forza` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `reddit_forzatune` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |
| `forza_horizon_hub` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_collector` | unavailable: HTTP network error; no stale data reused. |
| `forza_labs_map` | unavailable: HTTP network error; no stale data reused. |
| `escorenews_fh6` | unavailable: HTTP 403; no stale data reused. |
| `dungg_playlist` | no_current_item: HTTP 200; no fresh material used for this presentation-only update. |

## 2026-09-24T22:51:27+07:00 — русско-английский интерфейс сводки

- Повторно использован полный свежий аудит источников Winter от 22:35:17+07:00: он подтверждает активный сезон, а карточные факты, решения, ссылки и таймер не менялись.
- Для всех 14 карточек добавлен проверяемый английский перевод в `data/current-season.json`; русский остаётся исходным и языком по умолчанию.
- В веб-сводке добавлен переключатель RU/EN в отдельной строке шапки. Выбор хранится локально в браузере; на 375 px шапка без горизонтальной прокрутки.
- Визуалы не менялись: точные Winter-плитки всё ещё отсутствуют, Daily остаётся текстовым списком без публичного скриншота.

### Уточнение интерфейса

- Английский режим также переводит подписи источников, блок поддержки, статистику и график аудитории; ссылки и игровые факты не изменялись.

## 2026-09-25T04:47:18+07:00 — Winter Series 5: аудит перед подключением Boosty

- Официальная Festival Playlist открыта повторно и подтверждает активную `British Automotive — Winter` до 1 октября 2026; карточные факты сезона не менялись.
- Перепроверены все 16 обязательных источников. В источниках без нового материала текущей недели не использовались старые решения, изображения или коды тюнинга.
- Визуалы всех 14 активностей перепроверены: `confirmed=0`, `community=0`, `preliminary=0`, `missing=14`. Точных внутриигровых Winter-плиток не найдено; Daily остаётся текстовым списком без публичного визуала.
- В публичный блок поддержки добавлен Boosty: русский режим показывает Сбер / СБП и Boosty, английский — только Boosty. Содержимое карточек и Steam-зеркало от этого не меняются.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: страница не отдалась средству проверки; устаревшие данные не использовались. |
| `fandom_current` | unavailable: страница не отдалась средству проверки; устаревшие данные не использовались. |
| `forza_playlist` | checked: официальная Playlist подтверждает British Automotive — Winter, 24 сентября – 1 октября. |
| `forza_news` | no_current_item: лента открылась; нового детерминированного материала недели для карточек не найдено. |
| `forza_support_release_notes` | unavailable: раздел не отдался средству проверки; устаревшие данные не использовались. |
| `forza_support_known_issues` | no_current_item: страница Known Issues открылась; нового подтверждённого изменения для активностей не найдено. |
| `forza_forums_official` | no_current_item: официальный форум открылся; нового объявления, меняющего текущие карточки, не найдено. |
| `reddit_forzahorizon` | no_current_item: свежего подтверждённого breakdown Winter не найдено. |
| `reddit_forzahorizon6` | no_current_item: свежего подтверждённого Winter-материала для заполнения unknown-полей не найдено. |
| `reddit_forza` | no_current_item: свежего Information Thread с новыми фактами Winter не найдено. |
| `reddit_forzatune` | no_current_item: свежих подтверждённых тюнингов текущей недели не найдено. |
| `forza_horizon_hub` | no_current_item: сайт открылся; нового недельного решения или точной плитки не найдено. |
| `forza_labs_collector` | no_current_item: инструмент открылся; подтверждённого нового решения collectibles не найдено. |
| `forza_labs_map` | no_current_item: карта открылась; новых точных зимних плиток или решений не найдено. |
| `escorenews_fh6` | unavailable: страница не отдалась средству проверки; устаревшие данные не использовались. |
| `dungg_playlist` | unavailable: плейлист не отдался средству проверки; маршрут или решение не выводились. |

## 2026-09-25T05:18:00+07:00 — Winter Series 5: пользовательские точные плитки

- Повторная живая проверка всех 16 обязательных источников: официальная Playlist (`HTTP 200`) вновь подтвердила `British Automotive — Winter` до 1 октября 2026. Данные карточек, решения и тюнинги не менялись.
- Сохранены четыре неизменённых пользовательских скриншота в `reports/assets/series-05-winter/evidence/`. Из них без ретуши и без подложек вырезаны 12 точных зимних плиток: Weekly Jaguar, Photo, Treasure Hunt, два Championship, четыре PR, Trial и две Horizon Play.
- Daily намеренно не получил плитку: это объединённый текстовый блок. Его скриншот не использовался и не запрашивается.
- Для Monthly Rivals использована уже сохранённая локальная точная плитка `Спринт по Симанояме` (`tile-monthly-rivals-existing.webp`) по прямому указанию пользователя; новый скриншот не требовался.
- Визуальный аудит: `confirmed=0`, `community=13`, `preliminary=0`, `missing=1` (только Daily).

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: HTTP 403; устаревшие данные не использовались. |
| `fandom_current` | unavailable: HTTP 403; устаревшие данные не использовались. |
| `forza_playlist` | checked: HTTP 200; British Automotive — Winter подтверждён. |
| `forza_news` | no_current_item: HTTP 200; нового детерминированного факта недели не найдено. |
| `forza_support_release_notes` | unavailable: HTTP 404; устаревшие данные не использовались. |
| `forza_support_known_issues` | no_current_item: HTTP 200; нового влияния на плейлист не найдено. |
| `forza_forums_official` | no_current_item: HTTP 200; нового объявления, меняющего карточки, не найдено. |
| `reddit_forzahorizon` | unavailable: HTTP 403; решения и тюнинги не переносились. |
| `reddit_forzahorizon6` | unavailable: HTTP 403; решения и тюнинги не переносились. |
| `reddit_forza` | unavailable: HTTP 403; решения и тюнинги не переносились. |
| `reddit_forzatune` | unavailable: HTTP 403; тюнинги не переносились. |
| `forza_horizon_hub` | no_current_item: HTTP 200; нового недельного решения не найдено. |
| `forza_labs_collector` | no_current_item: HTTP 200; подтверждённого нового решения collectibles не найдено. |
| `forza_labs_map` | no_current_item: HTTP 200; нового точного визуала или решения не найдено. |
| `escorenews_fh6` | unavailable: HTTP 403; устаревшие данные не использовались. |
| `dungg_playlist` | no_current_item: HTTP 200; нового подтверждённого Winter-видео не найдено. |

## 2026-09-25T06:45:00+07:00 — Winter Series 5: новые решения и уточнения

- Живая официальная Playlist вновь подтверждает `British Automotive — Winter` до 1 октября 2026.
- Закрыты точные условия Weekly Jaguar, место Photo Challenge, место Treasure Hunt и третий маршрут Country Pickups. Добавлены свежие 9-значные коды тюнингов для Weekly, Country Pickups, Cult Street, четырёх PR-заездов и Trial.
- Исправлены ограничения: Cult Street — `D 400`; Drift Attack — `A 700` и 3 очка; Danger Sign — `B 600`; Speed Zone, Trailblazer и Trial — `A 700`.
- У Cult Street оставлен явный конфликт маршрутов: два свежих Winter-гида расходятся по одному заезду; маршрут не выбран без игрового/официального подтверждения.
- Визуалы не менялись: `community=13`, `missing=1` (Daily). Daily остаётся текстовым списком без публичной плитки.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: текущая категория не отдалась средству проверки; устаревшие данные не использовались. |
| `fandom_current` | unavailable: HTTP 402; устаревшие данные не использовались. |
| `forza_playlist` | checked: HTTP 200; British Automotive — Winter подтверждён. |
| `forza_news` | no_current_item: HTTP 200; нового детерминированного факта для карточек не найдено. |
| `forza_support_release_notes` | unavailable: раздел не отдался средству проверки; устаревшие данные не использовались. |
| `forza_support_known_issues` | no_current_item: HTTP 200; нового изменения плейлиста не найдено. |
| `forza_forums_official` | no_current_item: HTTP 200; форум переведён на общую информационную страницу, нового weekly-анонса нет. |
| `reddit_forzahorizon` | checked: свежий Winter breakdown подтвердил Weekly, Daily, ограничения и маршруты. |
| `reddit_forzahorizon6` | checked: свежий Winter-гайд дал место Photo, третий маршрут Country Pickups и коды тюнингов. |
| `reddit_forza` | checked: свежий Information Thread подтвердил ограничения и коды Country Pickups, Cult Street и Trial. |
| `reddit_forzatune` | no_current_item: свежего поста с решениями именно Winter-недели не найдено. |
| `forza_horizon_hub` | no_current_item: нового weekly-решения не найдено. |
| `forza_labs_collector` | no_current_item: текущего решения Winter Treasure Hunt не найдено. |
| `forza_labs_map` | no_current_item: новой точной Winter-плитки или карты сундука не найдено. |
| `escorenews_fh6` | unavailable: страница не отдалась средству проверки; устаревшие данные не использовались. |
| `dungg_playlist` | no_current_item: нового подтверждённого Winter-видео не найдено. |

## 2026-09-25T08:07:00+07:00 — подтверждение текущих данных и повторный аудит визуалов

- Официальная Playlist повторно подтверждает Series 5 British Automotive — Winter (24 сентября — 1 октября); текущий номер недели и дедлайн совпадают с `data/current-season.json`.
- Свежий пост r/ForzaHorizon от 24 сентября повторно подтверждает задания Weekly/Daily, Bamboo Forest Photo Challenge и Shimanoyama Treasure Hunt. Escorenews опубликовал карту сундука и статьи по Photo Challenge и Trial 24 сентября; использованы лишь ссылки/решения этой недели.
- Визуальный повторный аудит: точные локальные сезонные плитки присутствуют у 13 активностей, Daily намеренно текстовый и остаётся без публичной плитки (`community=13, preliminary=0, missing=1`). Хэши 13 активов сверяются в audit.json; новые изображения не подменялись.
- Найден дефект представления, не игровых данных: EN-локализация вставляла PI строками вроде `A 700` после генерации базовой HTML, поэтому английская версия теряла цветной бейдж. Исправлен общий языковой рендерер; в Steam устранены внутренние kind-маркеры и повтор заголовков.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live Fandom не отдал страницу; старые данные не использовались. |
| `fandom_current` | unavailable: live Fandom не отдал страницу; старые изображения/решения не переносились. |
| `forza_playlist` | checked: официальный список подтверждает British Automotive — Winter и дедлайн 1 октября. |
| `forza_news` | no_current_item: страница открывается, отдельного нового weekly-факта для карточек не обнаружено. |
| `forza_support_release_notes` | unavailable: раздел Release Notes не отдался; влияние патча не предполагалось. |
| `forza_support_known_issues` | no_current_item: статья доступна; нового влияния на активности недели не выявлено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую страницу форумов; нового объявления не найдено. |
| `reddit_forzahorizon` | checked: свежий пост от 24 сентября сверяет Weekly, все семь Daily, Photo и Treasure. |
| `reddit_forzahorizon6` | no_current_item: страница Reddit не показала свежего материала текущей недели. |
| `reddit_forza` | no_current_item: не подтверждён новый current-week information thread. |
| `reddit_forzatune` | no_current_item: нового тюнинг-поста этой недели не найдено. |
| `forza_horizon_hub` | no_current_item: доступен, нового точного weekly-решения не найдено. |
| `forza_labs_collector` | no_current_item: доступен, новых подтверждённых collectibles этой недели нет. |
| `forza_labs_map` | no_current_item: доступна, отдельной точной weekly-плитки не найдено. |
| `escorenews_fh6` | checked: материалы Winter Treasure, Photo и Trial датированы 24 сентября; использованы ссылки на сундук и фото-локацию. |
| `dungg_playlist` | no_current_item: свежий Winter-выпуск не подтверждён. |

## 2026-09-25T08:20:00+07:00 — проверка локализации и Steam после повторной публикации

- Повторно подтверждённый активный период: British Automotive — Winter, до 01.10.2026 21:30 Asia/Krasnoyarsk. Проверено 14 карточек; визуалы без изменений (`community=13, preliminary=0, missing=1` — Daily без публичной плитки).
- В EN-режиме сайта обнаружены два уровня потери PI-плашек: перевод подставлял простой текст вместо исходных badge-узлов, а первая реализация постобработки имела неверное экранирование в шаблонной строке HTML. Исправлена экранировка; после генерации проверяется публичное отображение.
- Steam-редактор подтверждает сохранение русской недели с понятными заголовками без kind-маркеров. Создание следующего раздела заблокировано Steam: руководство ожидает автоматическую проверку контента, UI возвращает Failure code 15. Не обходили проверку и не повторяли добавление. Английский файл с локалью готов, но английская секция публично отсутствует.
- В Steam PI намеренно остаётся простым текстом класса и рейтинга; CSS-цветная плашка применяется к веб-отчёту, Steam BBCode не поддерживает HTML-компонент сводки.

## 2026-09-25T10:52:00+07:00 — визуальное выделение кодов тюнинга

- Повторная живая проверка официальной Playlist подтверждает British Automotive — Winter до 1 октября 2026. В свежих r/ForzaHorizon, r/ForzaHorizon6 и r/forza от 24 сентября найдены текущенедельные материалы; Escorenews опубликовал Winter-карты Photo и Treasure 24 сентября. Fandom заблокирован robots, официальный Release Notes доступен (обновление 7 сентября, новых заметок текущей недели нет), Known Issues перечисляет июльские пункты без нового weekly-изменения; официальный форум показывает закрытие/перенос сообщества, новых официальных объявлений нет. Reddit r/ForzaTune и DungG не дали подтверждённого материала текущей недели; YouTube fetch ограничен. Forza Horizon Hub открыт, но его playlist-данные отстают; ForzaLabs Collector Tool и карта открываются, новых weekly collectibles/точных плиток нет. Старые решения не переносились.
- Проверка каждого visual и `automation/audit_visual_evidence.ps1`: точные локальные пользовательские плитки у 13 активностей, 0 preliminary, Daily намеренно текстовый без публичного visual (`community=13, preliminary=0, missing=1`). SHA-256 всех 13 плиток записаны в audit.json; очередь выдаёт `VISUAL_QUEUE_STATUS=READY`.
- Причина плохого отображения кодов: генератор сайта форматировал только числовую строку, уже заключённую во входной `<code>`, тогда как все RU/EN tune поля содержат обычный текст. Steam renderer также печатал девятизначный код внутри обычной строки автомобиля. Исправлены веб-рендер RU/EN и Steam: каждый код становится выделяемым семантическим code-чипом (`<code>` / `[code]`) с нормализацией пробелов `NNN NNN NNN`; кнопок копирования не добавлено. Инструкции AGENTS/skill/workflow уточнены; устаревшая инструкция о кнопке копирования удалена.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: robots.txt блокирует live Fandom; сезонные данные оттуда не использованы. |
| `fandom_current` | unavailable: доступная выдача Fandom не подтвердила точную страницу Winter FH6; старые плитки не переиспользовались. |
| `forza_playlist` | checked: официальный список подтверждает British Automotive — Winter (24 сентября — 1 октября). |
| `forza_news` | no_current_item: Series News о British Automotive от 7 сентября доступна; нового объявления текущей недели нет. |
| `forza_support_release_notes` | no_current_item: Release Notes от 7 сентября доступны через Known Issues; нового патча текущей недели не найдено. |
| `forza_support_known_issues` | no_current_item: живая статья доступна; недавнего Playlist-impacting изменения не обнаружено. |
| `forza_forums_official` | no_current_item: старый форум закрыт/перенаправляет на текущую страницу сообщества; свежего официального weekly-анонса не обнаружено. |
| `reddit_forzahorizon` | checked: свежий Winter breakdown от 24 сентября содержит текущие задания, Daily и решения. |
| `reddit_forzahorizon6` | checked: свежий Winter-гайд от 24 сентября подтверждает период, награды и карточки. |
| `reddit_forza` | checked: Information Thread Series 5 Winter опубликован 24 сентября. |
| `reddit_forzatune` | no_current_item: поиск не выявил отдельного Winter-поста; коды этой недели из этого источника не брались. |
| `forza_horizon_hub` | no_current_item: сайт открыт, но текущая витрина Playlist указывает старые данные; актуальных решений оттуда не взято. |
| `forza_labs_collector` | no_current_item: инструмент открыт; нового подтверждённого Winter collectible нет. |
| `forza_labs_map` | no_current_item: интерактивная карта открыта; отдельной точной плитки текущей недели не найдено. |
| `escorenews_fh6` | checked: статьи от 24 сентября подтверждают Winter Bamboo Forest Photo Challenge и Shimanoyama Treasure location. |
| `dungg_playlist` | unavailable: прямое чтение YouTube throttled; свежий Winter-выпуск подтвердить не удалось. |
## 2026-09-26T07:14:55+07:00 — повторный запуск Winter Series 5

- Официальная Playlist подтверждает `British Automotive — Winter` (24 сентября — 1 октября 2026); активный сезон совпадает с `data/current-season.json`. Полный список из семи Daily сверен с актуальными публикациями r/ForzaHorizon и r/ForzaHorizon6; будущие условия уже внесены в карточку.
- Официальная Playlist указывает маршрут Cult Street: Rainbow Bridge Descent, Okishinaimura Run, Norikura Descent. Уточнение первичного источника разрешило прежний конфликт маршрутов; закрыт `openItem` для Cult Street, `missingFields` очищен, completeness переведён в confirmed.
- Обновлены ссылки Photo Challenge и Treasure Hunt на отдельные карты Escorenews от 24 сентября. Уточнено краткое описание сундука по новой карте; неизвестные подробности не добавлялись.
- Визуально проверены все 14 активностей: 13 точных плиток из неизменённых пользовательских скриншотов, 0 confirmed, 13 community, 0 preliminary, 1 missing. Daily намеренно остаётся текстовым блоком без публичной плитки. SHA-256 13 локальных файлов проверен для audit.json; замен прошлой недели нет.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live Category:Series_(FH6) недоступна через браузерную проверку; устаревшие данные не использовались. |
| `fandom_current` | unavailable: текущая Series/Season страница Fandom недоступна; старые решения и визуалы не переносились. |
| `forza_playlist` | checked: официальный список подтверждает British Automotive — Winter, 24.09–01.10; также разрешает маршрут Cult Street. |
| `forza_news` | no_current_item: страница открывается; последняя новость British Automotive датирована 7 сентября, отдельной новости текущей недели нет. |
| `forza_support_release_notes` | no_current_item: раздел Release Notes недоступен напрямую, но Known Issues показывает последнюю запись FH6 от 7 сентября; новых заметок текущей недели не найдено. |
| `forza_support_known_issues` | no_current_item: страница просмотрена; актуальная статья не содержит нового влияющего на эту Playlist пункта. |
| `forza_forums_official` | no_current_item: официальный адрес перенаправляет на уведомление о закрытии форумов; нового weekly-анонса нет. |
| `reddit_forzahorizon` | checked: свежий Winter breakdown подтверждает Weekly, семь Daily, условия и ограничения; маршрутный список сверялся с официальной Playlist. |
| `reddit_forzahorizon6` | checked: текущенедельный Winter-гайд подтверждает активность, условия и тюнинги; его прежний конфликт Cult Street снят официальным маршрутом. |
| `reddit_forza` | checked: Winter Information Thread Series 5 опубликован 24 сентября; условия, маршруты и коды отмечены как сообщество. |
| `reddit_forzatune` | no_current_item: свежего FH6-поста именно для Winter текущей недели не найдено; коды из старых публикаций не использовались. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но его сезонный блок показывает устаревшую Series 1; текущие решения оттуда не брались. |
| `forza_labs_collector` | no_current_item: инструмент коллекции доступен; свежей карточки weekly-collectible этой недели не обнаружено. |
| `forza_labs_map` | no_current_item: карта доступна, отдельного подтверждённого визуала/решения Winter из неё не найдено. |
| `escorenews_fh6` | checked: опубликованы Winter-карты Treasure Hunt и Photo Challenge 24 сентября, а также гайд Trial; ссылки Photo/Treasure обновлены на текущие материалы. |
| `dungg_playlist` | unavailable: YouTube throttled чтение заданного плейлиста; Winter-выпуск подтвердить не удалось. |

## 2026-09-26T07:39:31+07:00 — английские игровые плитки Series 5 Winter

- Официальная Festival Playlist открыта повторно и подтверждает Series 5 `British Automotive — Winter`, 24 сентября — 1 октября 2026; англоязычные названия и порядок карточек сверены по строкам Winter в официальном списке.
- Проведён отдельный поиск изображения Monthly Rivals `Shimanoyama Sprint`: официальная Playlist, свежие публикации Reddit, недельные статьи и image search подтверждают событие и автомобиль 2025 McLaren W1, но не дают пригодной отдельной английской игровой плитки. Найденный ForzaLabs промо-постер гонки не является игровой плиткой и не использован. Для этой активности вырезана точная плитка из пользовательского англоязычного скриншота с COMPLETE.
- Все остальные 12 публичных игровых плиток заменены англоязычными версиями из четырёх приложенных скриншотов. Четыре оригинала сохранены в `reports/assets/series-05-winter/evidence/`; подготовлены 13 локальных точных кропов без изменения изображения внутри плиток. В state обновлены `visual.image`, `visual.sourceImage` и происхождение. Изображения используются общими для русского и английского вариантов сводки, поэтому на обеих языковых версиях теперь виден английский текст самой игры.
- Daily остаётся текстовым списком без публичной плитки по проектному правилу. Визуальная сводка: `confirmed=0, community=13, preliminary=0, missing=1` (единственный `missing` — намеренно текстовый Daily, не отсутствующая игровая плитка); незакрытых точных игровых плиток нет.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live Category:Series_(FH6) недоступна через веб-проверку; старые изображения и решения не использовались. |
| `fandom_current` | unavailable: корневая страница Fandom вернула HTTP 402; старые сезонные данные не использовались. |
| `forza_playlist` | checked: официальная страница открыта 26 сентября; подтверждает активную Winter-неделю, английские названия, Monthly Rivals `Shimanoyama Sprint` и автомобиль `2025 McLaren W1`. |
| `forza_news` | no_current_item: официальный индекс проверен; отдельной новости Festival Playlist за текущую неделю не найдено. |
| `forza_support_release_notes` | no_current_item: раздел не открылся напрямую; список Known Issues показывает последние FH6 Release Notes от 7 сентября, обновления за неделю 24–26 сентября нет. |
| `forza_support_known_issues` | no_current_item: живая статья проверена; нового пункта текущей недели, влияющего на активности, не найдено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую страницу Forza; weekly-анонса в ней нет. |
| `reddit_forzahorizon` | checked: пост Winter Breakdown от 24 сентября проверен; содержит текущие активности, включая Monthly Rivals. |
| `reddit_forzahorizon6` | checked: гайд Series 5 Winter от 24 сентября проверен; подтверждает Monthly Rivals и остальные текущие карточки. |
| `reddit_forza` | checked: Winter Information Thread Series 5 от 24 сентября проверен; подтверждает событие и чистый круг на 2025 McLaren W1. |
| `reddit_forzatune` | no_current_item: live subreddit проверен, отдельного текущенедельного FH6-поста с новыми решениями не обнаружено. |
| `forza_horizon_hub` | no_current_item: сайт открыт, но актуальный список Winter-активностей там не подтверждён; визуалы оттуда не брались. |
| `forza_labs_collector` | no_current_item: Collector Tool открыт; точной текущенедельной плитки или collectible-решения нет. |
| `forza_labs_map` | no_current_item: Interactive Map открыта; отдельная актуальная игровая плитка Monthly Rivals не найдена; промо-постер трассы не использован. |
| `escorenews_fh6` | checked: индекс не открылся, но текущие статьи Winter Photo Challenge и Treasure Hunt от 24 сентября проверены напрямую; только для карт и маршрутов. |
| `dungg_playlist` | unavailable: страница YouTube-плейлиста не загрузилась через веб-проверку; свежий Winter-выпуск подтвердить нельзя. |

## 2026-09-27T08:14:22+07:00 — ежедневная проверка Series 5 Winter и Steam-кодов

- Живая официальная Festival Playlist повторно подтверждает `British Automotive — Winter` (24 сентября — 1 октября 2026); состояние остаётся той же неделей, дедлайн `2026-10-01T21:30:00+07:00`. Новые подтверждённые факты карточек или решений для переноса в state не выявлены; `openItems` не изменены.
- Для полного английского списка условий использован свежий Winter Information Thread r/forza от 24 сентября; гайд r/ForzaHorizon6 от 24 сентября подтверждает текущие условия, а гайды по тюнингу от 25 сентября сверены как свежие community evidence. В r/ForzaTune свежую отдельную FH6-публикацию текущей недели подтвердить не удалось; коды из устаревших публикаций не переносились.
- Повторная визуальная сверка состояния: 13 отдельных игровых плиток (community; оригиналы пользовательских скриншотов 26 сентября и точные локальные кропы), 0 confirmed, 0 preliminary; Daily намеренно текстовая карточка без визуала (1 missing по контракту, скриншот не требуется). Новых пригодных текущенедельных плиток сверх пользовательских английских скриншотов не найдено.
- По запросу пользователя изменён только формат Steam-кода: непосредственно после последней цифры share code точка не выводится. Исправлено в общем RU/EN-рендерере и добавлено в правила проекта. Оба Steam-файла пересозданы; публикация в Steam не повторялась, так как предыдущая отправка русского раздела получила `Failure code: 15` и Steam показывал автоматическую проверку содержимого.
- Visual inventory: `confirmed=0, community=13, preliminary=0, missing=1` (Daily — намеренно текстовый; отдельной незакрытой плитки нет).

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) недоступна через браузерную проверку; старые решения не использовались. |
| `fandom_current` | unavailable: корень Fandom вернул HTTP 402; старые решения и визуалы не использовались. |
| `forza_playlist` | checked: [официальная Festival Playlist](https://forza.net/fh6playlists) открыта сегодня; подтверждает British Automotive — Winter, английские названия, порядок, Weekly, Daily, Monthly Rivals и дедлайн 1 октября. |
| `forza_news` | no_current_item: официальный индекс открыт; отдельной новости Playlist за текущую неделю не обнаружено. |
| `forza_support_release_notes` | unavailable: раздел release notes не открылся напрямую; доступная последняя FH6-запись — 7 сентября, новой недели/патча нет. |
| `forza_support_known_issues` | no_current_item: официальная страница открылась; новой записи текущей недели, меняющей условия проверенных карточек, не обнаружено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую страницу Forza; актуального weekly-анонса нет. |
| `reddit_forzahorizon` | checked: [Winter breakdown Series 5](https://www.reddit.com/r/ForzaHorizon/comments/1wp1p0o/fh6_series_5_winter_breakdown_and_rewards/) от 24 сентября подтверждает активности и награды. |
| `reddit_forzahorizon6` | checked: [Winter playlist guide](https://www.reddit.com/r/ForzaHorizon6/comments/1wozwwv/fh6_series_5_winter_festival_playlist_guide/) от 24 сентября и community tuning guide от 25 сентября проверены. |
| `reddit_forza` | checked: [Winter Information Thread](https://www.reddit.com/r/forza/comments/1wp7bpn/fh6_winter_information_thread_series_5/) от 24 сентября содержит полный список активностей и сезонные награды. |
| `reddit_forzatune` | no_current_item: subreddit проверен; отдельной публикации тюнингов FH6 за текущую неделю не найдено. Свежие коды из соседних subreddit отдельно сверены, не приписаны этому источнику. |
| `forza_horizon_hub` | no_current_item: сайт открылся, но свежего подтверждения карточек Series 5 Winter для изменений state не обнаружено. |
| `forza_labs_collector` | no_current_item: Collector Tool открылся; отдельного нового Winter collectible-решения или игровой плитки нет. |
| `forza_labs_map` | no_current_item: Interactive Map открылась; самостоятельной точной игровой плитки для этой недели нет. |
| `escorenews_fh6` | unavailable: индекс Escorenews не открылся сегодня; старые карты не использовались как новое подтверждение. |
| `dungg_playlist` | unavailable: YouTube playlist недоступен в браузерной проверке; выпуск текущей недели подтвердить нельзя. |

## 2026-09-27T08:32:08+07:00 — пунктуация tuning share codes

- По просьбе пользователя убрана точка непосредственно после девятизначных tuning share codes во всех русских и английских значениях `tuneHtml` в единственном редактируемом источнике `data/current-season.json`. Другие знаки пунктуации и текст рекомендаций не менялись.
- Правило уточнено для GitHub HTML и Steam в `.agents/skills/fh6-season-maintainer/SKILL.md` и `AGENTS.md`. Предыдущая живая проверка всех обязательных источников и 13 отдельных плиток текущей недели Series 5 Winter выполнена 08:14 и остаётся в пределах четырёхчасового окна; новые факты, визуалы и коды решений не добавлялись. Daily по-прежнему намеренно текстовый.
- Проверка после генерации должна подтвердить, что ни один из 16 рекомендационных кодов RU/EN не заканчивается точкой в HTML или Steam mirrors; запрещённые Steam `[code]` и copy-кнопки не вводятся.

## 2026-09-27T08:40:21+07:00 — читаемые типы активностей в сводке

- По замечанию пользователя заменён вывод технического `kind` на локализованные названия типов в русском и английском интерфейсе GitHub-сводки. Добавлены явные подписи для всех используемых типов (`weekly`, `daily`, `photo`, `treasure_hunt`, `championship`, `pr`, `trial`, `horizon_play`, `monthly_rivals`) и человекочитаемый fallback, превращающий неизвестный ID в слова без подчёркиваний.
- Содержимое карточек, порядок, плитки, тюнинги и сведения сезона не менялись. Все 16 обязательных источников и 14 визуальных записей сверены в полном аудите 08:14:22 +07:00; этот аудит остаётся свежим в четырёхчасовом окне guard. Подтверждённая активная неделя — Series 5 British Automotive, Winter; дедлайн 2026-10-01 21:30 +07:00. Daily остаётся намеренно текстовым.
- Визуальный итог без изменений: `confirmed=0, community=13, preliminary=0, missing=1` (Daily — намеренно текстовая карточка). Текущие плитки повторно сопоставлены с английскими пользовательскими игровыми скриншотами; новые визуальные assets не добавлялись.

## 2026-09-27T08:49:55+07:00 — читаемость легенды графика

- По замечанию к публичной сводке убраны подписи GitHub/Steam из области линий. Текущие значения вынесены в отдельную легенду над SVG-графиком с цветовыми образцами, а область данных немного сдвинута вниз; итоговые подписи больше не пересекают линии и конечные точки.
- Сезонные факты, карточки и визуалы не менялись. Полный аудит 16 источников и всех 14 визуальных записей от 08:14:22 +07:00 ещё действителен в четырёхчасовом окне guard; Series 5 British Automotive — Winter, дедлайн 2026-10-01 21:30 +07:00. Daily остаётся намеренно текстовым.
- Текущая визуальная сводка без изменений: `confirmed=0, community=13, preliminary=0, missing=1` (Daily без публичной плитки). Новых игровых изображений или источников фактов не добавлялось.

## 2026-09-27T08:58:39+07:00 — ссылки в Steam RU/EN

- По текущему запросу сверены обе локально сгенерированные Steam-секции. В каждой ссылки присутствуют только на полную GitHub-сводку (в начале и в конце) и на две полезные карты текущих локаций Photo Challenge и Treasure Hunt в финальном блоке ссылок; прочих внешних ссылок в тексте карточек нет. Ссылки остаются кликабельными с описательным текстом, без показа сырых URL.
- Уточнены `AGENTS.md` и skill-правила: запрещены ссылки на источники/сообщество и любые иные URL в Steam. Рендерер получил allowlist-проверку URL и проверку, что ссылки локаций располагаются только в заключительном блоке. Контент карточек и список допустимых ссылок не менялись.
- Для сезонной части используется полный аудит 16 обязательных источников от 08:14:22 +07:00, ещё свежий для текущего guard-запуска; статусы каждого источника перечислены в предыдущей датированной записи. Живая официальная Playlist подтверждает Series 5 British Automotive — Winter, дедлайн `2026-10-01T21:30:00+07:00`. Визуальный аудит 14 activities: `confirmed=0, community=13, preliminary=0, missing=1` (Daily намеренно без плитки). Новые сезонные факты/визуалы не добавлялись.
## 2026-09-27T10:47:03+07:00 — UX-аудит отчёта Series 5 Winter (fh6-20260927-103956-585082)

- Живая официальная Festival Playlist подтверждает Series 5 `British Automotive — Winter`, 24 сентября — 1 октября 2026; текущий `season.endAt` остаётся `2026-10-01T21:30:00+07:00`. Это не rollover.
- Внесены только согласованные улучшения представления: адаптивное оглавление с переходами ко всем карточкам, более точное пояснение метрик, мобильная перестраиваемая легенда графика, уточнённая формулировка к Danger Sign. Сезон, награды, порядок карточек, условия и коды не менялись.
- Перепроверены все 14 визуальных записей: `community=13, confirmed=0, preliminary=0, missing=1`; единственный `missing` — предусмотренная контрактом текстовая карточка Daily, публичный скриншот ей не нужен. Все 13 отдельных плиток — текущей Winter-недели из сохранённых пользовательских английских снимков 26 сентября; соответствующие image/sourceImage присутствуют локально. Более точная текущенедельная замена в официальном наборе или проверенных статьях не обнаружена. Общие сезонные изображения не использовались.
- В карточке Azure Drive Danger Sign цель 689 ft (210 м) подтверждена официальной плиткой. Отдельный маршрут точного подъезда источники не подтверждают, поэтому новый текст оставляет эту часть явно непроверенной и больше не обещает, что её уточнит уже показанная плитка.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) вернула Internal Error при открытии; текущие сведения оттуда не брались. |
| `fandom_current` | unavailable: корень Fandom вернул Internal Error; старые сезонные сведения и визуалы не использовались. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; активны British Automotive — Winter (24 Sep–1 Oct), 14 карточек, Azure Drive B 600 / 689 ft, Weekly, Daily и Monthly Rivals подтверждены. |
| `forza_news` | no_current_item: официальный индекс Forza News проверен; отдельной публикации Playlist текущей недели не обнаружено. |
| `forza_support_release_notes` | no_current_item: прямая секция Release Notes не открылась; официальная Known Issues показывает последнюю FH6-заметку от 7 сентября, свежей записи этой недели не найдено. |
| `forza_support_known_issues` | no_current_item: официальная статья открыта; отмечены Known Issues июля и ссылка на обновляемый Feedback Portal, но свежей записи недели, меняющей эту Playlist, нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общую страницу Forza Forums; объявления этой недели не обнаружено. |
| `reddit_forzahorizon` | checked: Winter Breakdown от 24 сентября содержит текущие условия, награды, Daily и обсуждения Winter; также опубликован tuning guide 25 сентября. |
| `reddit_forzahorizon6` | checked: Winter Playlist guide от 24 сентября и отдельный Winter tuning guide от 25 сентября проверены; условия/советы относятся к этой неделе. |
| `reddit_forza` | checked: Winter Information Thread Series 5 от 24 сентября подтверждает награды и дату следующего сброса 1 октября 14:30 UTC; в том же сообществе найден свежий Winter tuning guide. |
| `reddit_forzatune` | no_current_item: раздел проверен; отдельной публикации FH6/Winter за текущую неделю не найдено, коды из других разделов не приписывались этому источнику. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но его weekly-блок всё ещё сообщает Series 1; контент оттуда не использован для фактов или плиток Series 5. |
| `forza_labs_collector` | unavailable: инструмент Collector Tool вернул Internal Error; новые сведения о collectible не извлекались. |
| `forza_labs_map` | no_current_item: Interactive Map доступна и содержит справочные маркеры карты, но отдельные данные/визуалы Winter этой недели не найдены. |
| `escorenews_fh6` | checked: индекс и текущие статьи доступны; материал Shimanoyama Treasure Hunt опубликован 24 сентября, также перечислены Winter Photo Challenge и Trial. Локации сверены, изображение сезонной статьи не подменяет игровую плитку. |
| `dungg_playlist` | unavailable: YouTube playlist не удалось открыть/проверить на свежий выпуск Winter; решения оттуда не использованы. |

## 2026-09-27T10:53:24+07:00 — повторная проверка UX-отчёта (fh6-20260927-105241-804556)

- Повторная живая Playlist подтверждает ту же Series 5 `British Automotive — Winter`, 24 сентября — 1 октября; смены сезона нет. Все активности и семь Daily сверены с официальным списком и свежими темами недели. Изменение текста Danger Sign остаётся ограниченным уточнением степени проверки: плитка показывает 689 ft, а конкретный оптимальный заход отдельно не подтверждён.
- UX-обновление сохранено: responsive-оглавление на основе 14 карточек с локализованными заголовками и якорями; Steam unique visitors отделены в подписи графика от GitHub page-counter hits (не уникальные посетители); HTML-легенда графика переносится на узком экране; Daily остаётся намеренно без визуала.
- Visual inventory повторно сверен локально: `community=13, confirmed=0, preliminary=0, missing=1`. Все 13 уникальных плиток текущей Winter-недели привязаны к локальным подготовленным кадрам и сохранённым полным скриншотам пользователя. `activity_02_daily` — намеренно текстовый блок, без запроса скриншота.
- Первый защищённый build этого UX-изменения остановился до публикации: проектный portable-проверяющий требует точное значение исходного subtitle в контракте диаграммы. Исходный subtitle артефакта возвращён без изменений; поясняющий текст останется в финальном HTML-слое, где пользователь его увидит. Публичная публикация первого запуска не выполнялась.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: ссылка категории недоступна через веб-проверку; новые сведения не брались. |
| `fandom_current` | unavailable: Fandom вернул HTTP 402; старые сезонные данные и визуалы не использовались. |
| `forza_playlist` | checked: https://forza.net/fh6playlists подтверждает British Automotive — Winter, порядок активностей, все Daily, Azure Drive B 600 / 689 ft и дедлайн 1 октября. |
| `forza_news` | no_current_item: официальный индекс открыт; отдельного Playlist-поста на эту неделю нет. |
| `forza_support_release_notes` | unavailable: настроенная секция не открылась; релизную заметку текущей недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: официальный список открыт; свежей записи недели, меняющей активности, не обнаружено. |
| `forza_forums_official` | no_current_item: тег ведёт на общие Forza Forums; текущего недельного объявления нет. |
| `reddit_forzahorizon` | checked: свежий Winter Breakdown и Winter tuning thread текущей недели проверены; новых исправлений условий для добавления не найдено. |
| `reddit_forzahorizon6` | checked: Winter guide и Winter tuning thread этой недели доступны и проверены. |
| `reddit_forza` | checked: Winter Information Thread и сезонные советы текущей недели проверены. |
| `reddit_forzatune` | no_current_item: сообщество доступно, отдельной FH6-публикации этой недели не найдено. |
| `forza_horizon_hub` | no_current_item: ресурс всё ещё показывает Series 1 в weekly-блоке; для Series 5 не использован. |
| `forza_labs_collector` | no_current_item: Collector Tool открылся, но недельных данных текущей Series/нового collectible не показывает. |
| `forza_labs_map` | no_current_item: Interactive Map открылась, подтверждённой сезонной плитки или нового решения Winter нет. |
| `escorenews_fh6` | unavailable: индекс не открылся в этой проверке; текущие статьи ранее найдены поиском, но новых утверждений поверх них не переносилось. |
| `dungg_playlist` | unavailable: YouTube playlist не загрузился; свежий выпуск Winter не подтверждён. |

## 2026-09-27T11:15:51+07:00 — социальные действия русской/английской сводки

- Живая Official Festival Playlist снова подтверждает Series 5 `British Automotive — Winter`, 24 сентября — 1 октября 2026; срок и карточки не менялись. Свежие текущенедельные темы r/ForzaHorizon, r/ForzaHorizon6 и r/forza проверены; новые факты в карточки не переносились. Forza News проверена, но отдельной публикации этой недели, меняющей Playlist, нет.
- Пользователь запросил лёгкие социальные действия в русской и английской версиях GitHub-отчёта: системное «Поделиться» на мобильном, копирование ссылки на ПК, форму уточнения/ошибки с выбором языка и активности и переход к комментариям руководства Steam. Реализация не собирает и не сохраняет сообщение на стороне сайта: форма лишь предварительно заполняет черновик публичного GitHub Issue; перед переходом указаны необходимость входа и публичность отзыва. Boosty и статистика остаются в нижнем блоке поддержки.
- Повторно выполнен `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`. Текущие локальные точные плитки не изменялись: `community=13, confirmed=0, preliminary=0, missing=1`; `activity_02_daily` остаётся намеренно текстовым без публичной плитки и без запроса скриншота. Все 13 отдельных кадров — актуальные Winter-плитки, ранее сопоставленные с сохранёнными полными пользовательскими скриншотами 26 сентября; новых или прошлосезонных изображений не добавлено.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) недоступна через текущий live fetch; новые сведения не использованы. |
| `fandom_current` | unavailable: корень Fandom вернул HTTP 402; сезонные факты оттуда не брались. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; Series 5 British Automotive — Winter (24 Sep–1 Oct), условия и порядок Playlist подтверждены. |
| `forza_news` | no_current_item: Forza News и материал Series 5 проверены; отдельного нового Playlist-материала этой недели не найдено. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes не открылась; свежую заметку этой недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: официальная Known Issues статья доступна; свежей записи этой недели, влияющей на текущие активности, не обнаружено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум; недельного объявления Playlist не найдено. |
| `reddit_forzahorizon` | checked: свежий Winter Breakdown от 24 сентября подтверждает условия Weekly/Daily, Photo и Treasure Hunt. |
| `reddit_forzahorizon6` | checked: текущий Winter guide от 24 сентября проверен, включая PR, Trial и советы этой недели. |
| `reddit_forza` | checked: Winter Information Thread Series 5 от 24 сентября и свежая сезонная публикация тюнингов проверены. |
| `reddit_forzatune` | no_current_item: отдельной публикации FH6/Winter за текущую неделю в этом сообществе не обнаружено; сторонние коды к нему не приписывались. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но актуального Winter-материала этой недели нет; старый Weekly блок не использован. |
| `forza_labs_collector` | no_current_item: Collector Tool доступен; свежего Winter collectible-подтверждения нет. |
| `forza_labs_map` | no_current_item: Interactive Map доступна; отдельного сезонного ответа или точной Playlist-плитки не обнаружено. |
| `escorenews_fh6` | unavailable: индекс Escorenews сейчас вернул ошибку загрузки; новые данные не извлечены. |
| `dungg_playlist` | unavailable: страница YouTube playlist не загрузилась; новый выпуск этой недели подтвердить нельзя. |

## 2026-09-27T21:02:36+07:00 — Steam: уменьшение ссылок и полный повторный аудит

- Гипотеза о ссылках как причине проверок: частично подтверждена официальной справкой Steam. Она говорит, что при подозрении на вредоносное содержимое ссылки временно скрываются на время автоматической проверки; также среди причин фильтрации названы free/less-common hosting domains. Это подтверждает правдоподобность, но не устанавливает причину конкретных проверок этого руководства и не гарантирует, что одиночная ссылка GitHub Pages не будет отфильтрована.
- Для снижения риска политика Steam изменена: один прямой GitHub URL остаётся в описании руководства перед содержанием; обе недельные секции RU/EN не содержат URL, Steam BBCode-ссылок, карт/локаций или цитирований источников. Карты и подсказки остаются в веб-сводке GitHub. Основное описание ещё не опубликовано через Steam; публичную проверку не заявляю.
- Живая официальная Playlist подтверждает Series 5 `British Automotive — Winter`, 24 сентября — 1 октября 2026; дедлайн без изменений `2026-10-01T21:30:00+07:00`. Изменений фактов карточек в этом запуске не внесено.
- Проверены визуалы всех 14 активностей: 13 индивидуальных актуальных плиток пользователя на английском языке, статусы `community=13`, `confirmed=0`, `preliminary=0`, `missing=1`; SHA-256 всех 13 prepared images записаны в audit.json. Daily остаётся намеренно текстовым блоком без плитки. Более точные отдельные плитки в живых источниках не найдены; старые изображения не переиспользованы. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`.
- Steam локальные генераторы пройдены: обе секции содержат 14 активностей в игровом порядке; RU — 3,715 знаков, EN — 3,331 (лимит 4,800); в секциях нет внешних URL и `[url=...]`. Main-description renderer проверил описание длиной 1,398 символов с ровно одним URL на настроенную сводку GitHub.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) вернула Internal Error; новые сезонные факты и плитки не использованы. |
| `fandom_current` | unavailable: корень Fandom вернул Internal Error; сезонные данные оттуда не брались. |
| `forza_playlist` | checked: официальная страница открыта; строки Series 5 Winter сверены по датам, всем 14 активностям, условиям и игровому порядку. |
| `forza_news` | no_current_item: официальный материал Series 5 от 7 сентября подтверждает серию, но новостей текущей недели по зимнему плейлисту не найдено. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes недоступна через live fetch; свежую запись текущей недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: официальный список проверен; текущенедельного изменения, затрагивающего Winter Playlist, не найдено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на страницу закрытия форумов/официальных каналов; текущенедельного объявления нет. |
| `reddit_forzahorizon` | checked: свежий Winter Breakdown от 24 сентября открыт; сверены условия, награды и ограничения текущей недели. |
| `reddit_forzahorizon6` | checked: свежий Winter Guide от 24 сентября открыт; подтверждены Weekly, Daily, PR Stunts, Trial и текущие советы. |
| `reddit_forza` | checked: Winter Information Thread от 24 сентября и сезонная tuning-тема от 25 сентября открыты; использованы как свежие источники недели. |
| `reddit_forzatune` | no_current_item: новая лента открыта; видимый релевантный FH6-пост старше текущей недели, нового тюнинга Winter за неделю 24–30 сентября нет. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но его weekly-раздел показывает Series 1; данные для Series 5 Winter не использованы. |
| `forza_labs_collector` | no_current_item: Collector Tool доступен как общий автомобильный каталог; недельного текущего collectible нет. |
| `forza_labs_map` | no_current_item: Interactive Map доступна как общий набор маркеров; Winter-ответ/плитка недели не опубликованы. |
| `escorenews_fh6` | checked: индекс недоступен, но адресно открыты статьи от 24 сентября по #BambooPerfect, Shimanoyama Treasure Hunt и Winter Rallies Trial. |
| `dungg_playlist` | unavailable: YouTube playlist live fetch вернул ошибку; свежий выпуск этой недели не подтверждён. |

## 2026-09-27T11:45:59+07:00 — полный аудит перед подтверждённым обновлением Steam

- Пользователь явно разрешил обновить Steam. Живая официальная Playlist подтверждает Series 5 `British Automotive — Winter`, 24 сентября — 1 октября 2026; текущий дедлайн `2026-10-01T21:30:00+07:00`, нового сезона нет. Условия и игровой порядок сверены по официальной таблице; отдельные свежие обсуждения текущей недели просмотрены, новых подтверждённых изменений к карточкам после предыдущей проверки не найдено. Карточки/коды/визуалы не изменены.
- Проверены все обязательные источники. Отсутствующие свежие материалы и недоступные страницы зафиксированы отдельно; старые материалы не переносились как текущие.
- Повторный аудит всех 14 visual: `community=13, confirmed=0, preliminary=0, missing=1`. 13 индивидуальных плиток — точные игровые Winter-кадры из сохранённых исходных пользовательских скриншотов и не менялись; Daily намеренно текстовый, публичная плитка/скриншот не нужны. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`.
- Steam-рендеры текущего состояния готовы: RU 4,265 знаков, EN 3,870, обе версии не превышают 4,800. Checker до публичного редактирования показал `UPDATE_REQUIRED` для RU и отсутствие подтверждённой публикации EN. Имена секций должны остаться ровно `Актуальная неделя · Русский` и `Current Week · English`; менять только существующие секции, не создавать дубликаты. В тексте Steam share codes остаются обычным текстом без пунктуации после последней цифры и без `[code]`.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) недоступна через live fetch; сведения и старые изображения не использовались. |
| `fandom_current` | unavailable: Fandom вернул HTTP 402; свежую сезонную страницу/плитки получить нельзя. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; Winter, срок, weekly, все семь Daily, Photo, Treasure, оба чемпионата, PR, Trial и Horizon Play сверены по строкам Series 5 Winter. |
| `forza_news` | no_current_item: официальный материал `Celebrate British Automotive` открыт (7 сентября) и подтверждает Series, но это не новая публикация текущей недели. |
| `forza_support_release_notes` | unavailable: настроенная секция Support вернула Internal Error; последняя видимая официальная запись — Series 5 release notes от 7 сентября, свежей записи недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: официальный список Known Issues открыт; список релизных заметок до 7 сентября, свежего изменения этой Playlist за неделю нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на страницу о закрытии форумов и официальных каналах; текущего форумного объявления нет. |
| `reddit_forzahorizon` | checked: свежий Winter Breakdown от 24 сентября открыт; подтвердил недельные условия, награды и PR-классы. |
| `reddit_forzahorizon6` | checked: Winter Festival Playlist Guide от 24 сентября открыт; также проверен сезонный tuning thread от 25 сентября. |
| `reddit_forza` | checked: Winter Information Thread Series 5 от 24 сентября открыт; подтверждает смену 1 октября и сезонные награды. |
| `reddit_forzatune` | no_current_item: текущая лента проверена; свежей публикации FH6/Winter за эту неделю не обнаружено. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но weekly-блок показывает Series 1; для Series 5 Winter не использовался. |
| `forza_labs_collector` | no_current_item: Collector Tool доступен как список автомобилей; данных Winter Playlist/недельных collectible нет. |
| `forza_labs_map` | no_current_item: Interactive Map доступна с общими маркерами локаций, но актуальной Playlist-плитки или Winter-ответа не содержит. |
| `escorenews_fh6` | checked: индекс проверен; найдены свежие текущенедельные материалы 24 сентября по #BambooPerfect, Shimanoyama Treasure Hunt и Winter Rallies Trial. Карты локаций пригодны как ссылки, но не заменяют игровые плитки. |
| `dungg_playlist` | unavailable: YouTube throttled live fetch; свежий выпуск текущей недели нельзя подтвердить. |

## 2026-09-28T06:14:13+07:00 — ежедневный аудит Winter Series 5

- Официальная Festival Playlist подтверждает Series 5 `British Automotive — Winter`, 24 сентября–1 октября 2026; активный сезон прежний, дедлайн `2026-10-01T21:30:00+07:00`. Проверены официальный список активностей и их порядок. Нового официального сезонного rollover нет.
- В карточке Treasure Hunt уточнён подход к сундуку по свежим материалам Escorenews и GamesHedge: южный Shimanoyama к западу от Tokyo City, ориентир Lake View Speed Trap у грунтовой дороги, рядом со стартом Taiyaki Scramble. Этот ориентир внесён синхронно в RU/EN поля решения; неизвестный точный поворот не придумывался.
- Проверены все 14 визуалов: `community=13, confirmed=0, preliminary=0, missing=1`. 13 отдельных англоязычных игровых плиток проверены по prepared-файлам и SHA-256; они остаются пользовательскими кадрами. Daily намеренно текстовый, без публичного изображения и без запроса скриншота. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`, `screenshotsRequired=0`.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: Category:Series_(FH6) недоступна через live fetch; сезонные факты и изображения оттуда не использованы. |
| `fandom_current` | unavailable: текущая страница Fandom недоступна через live fetch; старые сведения не переносились. |
| `forza_playlist` | checked: официальная Playlist открыта; подтверждены British Automotive Winter, даты 24 Sep–1 Oct и сезонные активности. |
| `forza_news` | no_current_item: официальный News индекс доступен; отдельной публикации текущей недели по Winter не найдено, материал Series 5 от 7 сентября не считался свежим. |
| `forza_support_release_notes` | unavailable: настроенная секция Support вернула Internal Error; обновление текущей недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: Known Issues открыта; последняя видимая дата обновления — 20 июля, связанных свежих сезонных исправлений нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум; публикации этой недели по Playlist не обнаружено. |
| `reddit_forzahorizon` | no_current_item: свежая лента открыта; текущенедельной публикации с новыми решениями именно для Playlist в проверенной ленте не найдено. |
| `reddit_forzahorizon6` | checked: проверены свежие Winter Guide и tuning guide от 24–25 сентября; условия и несколько tuning-рекомендаций текущей недели сверены, конфликтующих исправлений карточек нет. |
| `reddit_forza` | checked: открыт Winter Information Thread от 24 сентября; проверены дедлайн, Daily, награды и текущая недельная информация. |
| `reddit_forzatune` | no_current_item: текущая лента доступна, но FH6/Winter публикаций за 24–30 сентября не найдено. |
| `forza_horizon_hub` | no_current_item: сайт доступен, однако сезонной публикации Series 5 Winter текущей недели нет; старый weekly-блок не использован. |
| `forza_labs_collector` | no_current_item: Collector Tool открыт как общий каталог машин; подтверждённых данных о текущих сезонных collectibles нет. |
| `forza_labs_map` | no_current_item: Interactive Map открыта, но актуальной Playlist-разметки/плитки этой недели нет. |
| `escorenews_fh6` | checked: открыты свежие материалы от 24 сентября по #BambooPerfect и Shimanoyama Treasure Hunt; карта/текст сундука подтверждают южный край Shimanoyama западнее Tokyo City. Совместно с GamesHedge уточнены ориентиры Lake View Speed Trap и Taiyaki Scramble; старые коды не переносились. |
| `dungg_playlist` | unavailable: YouTube playlist не загрузилась через live fetch; новый выпуск текущей недели подтвердить нельзя. |

## 2026-09-29T06:47:31+07:00 — ручной ежедневный аудит Winter Series 5

- Живая официальная Playlist повторно подтверждает Series 5 `British Automotive — Winter`, период 24 сентября — 1 октября 2026 и текущий порядок активностей. Сезон не сменился; дедлайн остаётся `2026-10-01T21:30:00+07:00`. Официальные строки подтверждают ежедневное задание 29 сентября: получить минимум одну звезду на Speed Trap, Weekly Challenge (две Road Races на 2010 Jaguar C-X75), маршруты чемпионатов, PR-цели, Trial и Horizon Play.
- Новое уточнение Weekly Challenge: в комментариях к свежему Winter Information Thread игроки сообщали, что этап с двумя Road Races у некоторых не засчитывался; один комментарий от 28 сентября говорит, что ему понадобилось три заезда. Официальное условие остаётся двумя гонками. В решение RU/EN добавлено осторожное примечание попробовать третий заезд только если прогресс не засчитался; это наблюдение сообщества, не подтверждённый официальный баг.
- Новая тюнинг-рекомендация текущей недели: для Trial `Winter Rallies` опубликован дополнительный код Opel Manta 400 `947 504 263`; он добавлен как запасной рядом с уже указанным кодом `930 661 576`, без имени автора. Это независимая рекомендация сообщества, не заявляется как тест проекта.
- Проверены все 14 visual по карточкам и контрольным SHA-256: 13 индивидуальных англоязычных игровых плиток пользователя (`community=13`), `confirmed=0`, `preliminary=0`; Daily остаётся намеренно без публичной плитки (`missing=1`) и не требует скриншота. Более точные индивидуальные плитки в актуальных онлайн-источниках не обнаружены; старые плитки не переносились. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`, запросов скриншотов нет.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: категория FH6 Series недоступна через live fetch; сезонные факты и визуалы оттуда не использовались. |
| `fandom_current` | unavailable: корень Fandom вернул HTTP 402; актуальная сезонная страница не прочитана. |
| `forza_playlist` | checked: открыта официальная Playlist; сверены British Automotive Winter, даты, Daily 29 сентября, 14 активностей, условия, награды и маршруты. |
| `forza_news` | no_current_item: официальный News индекс проверен; новая публикация текущей недели о FH6 Winter Playlist не найдена. Новость Series 5 от 7 сентября не считалась свежей. |
| `forza_support_release_notes` | unavailable: заданная секция Release Notes вернула Internal Error; известна только прежняя публикация 7 сентября, обновление текущей недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: Known Issues открыта; видимое обновление датировано 20 июля, свежего Playlist-связанного исправления нет. Комментарии игроков о Weekly Challenge не приписываются официальному списку багов. |
| `forza_forums_official` | no_current_item: официальный форумный адрес перенаправляет на страницу об уходе с форумов; свежего объявления Playlist на заменивших каналах не найдено. |
| `reddit_forzahorizon` | checked: открыт свежий Winter Breakdown от 24 сентября; сверены задания и награды. Новых подтверждённых изменений условий кроме обсуждаемой проблемы Weekly Challenge не найдено. |
| `reddit_forzahorizon6` | checked: открыт свежий Winter Guide от 24 сентября; сверены 14 активностей, Daily и основные подсказки. В комментариях есть жалобы на незасчитывание этапа Road Races и единичный совет сделать третий заезд; оставлено как неподтверждённое наблюдение сообщества. |
| `reddit_forza` | checked: открыт Winter Information Thread от 24 сентября и свежая ветка seasonal tunes; подтверждены сезонные данные и добавлен альтернативный Trial tune `947 504 263`. |
| `reddit_forzatune` | no_current_item: свежая лента проверена; релевантной публикации FH6 Playlist/Winter за текущую неделю не найдено. Более старые настройки не переносились. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но weekly-блок всё ещё показывает Series 1; данные для Series 5 Winter не использованы. |
| `forza_labs_collector` | no_current_item: Collector Tool доступен как общий список машин; актуальных сезонных collectibles этой недели нет. |
| `forza_labs_map` | no_current_item: Interactive Map доступна как общий каталог маркеров, но свежей разметки/точной Playlist-плитки Winter не содержит. |
| `escorenews_fh6` | checked: открыты текущенедельные руководства от 24 сентября по #BambooPerfect и Treasure Hunt; Treasure подтверждает юго-запад Shimanoyama западнее Tokyo City. Новых материалов после этой недели не найдено. |
| `dungg_playlist` | unavailable: YouTube playlist live fetch вернул throttling; наличие свежего выпуска недели подтвердить нельзя. |

# 2026-09-30T07:38:20+07:00 — ручной полный аудит Winter Series 5

- Живая официальная Playlist повторно подтверждает Series 5 `British Automotive — Winter`, сезон 24 сентября — 1 октября 2026, и активность до 1 октября. Сегодняшнее Daily (30.09) — завершить один круг на любой Time Attack circuit; официальный список содержит все семь Daily. Смены сезона нет; дедлайн `2026-10-01T21:30:00+07:00`.
- Проверены свежие текущенедельные публикации Reddit и Escorenews. Новых подтверждённых изменений карточек/условий/наград и новых актуальных решений Treasure Hunt/Photo Challenge не обнаружено. В актуальном Winter-гайде Reddit есть предупреждение сообщества: ANNA Autopilot может пометить круг Monthly Rivals как грязный. Оно добавлено RU/EN к подсказке чистого круга с явной пометкой «неофициальное наблюдение», без объявления подтверждённого бага. Остальные решения и коды не менялись.
- Проверены все 14 записей визуала: 13 отдельных англоязычных текущих плиток пользователя и их исходные screenshot-evidence на месте, SHA-256 prepared/original файлов зафиксированы в audit.json; `community=13, confirmed=0, preliminary=0, missing=1`. Daily намеренно текстовый, без публичной плитки и без запроса скриншота. Более точных отдельных плиток недели в доступных онлайн-источниках не найдено. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`, запросов скриншотов нет.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: FH6 Series category вернула Internal Error; сезонные факты и визуалы оттуда не использовались. |
| `fandom_current` | unavailable: Fandom root вернул Internal Error; текущую страницу сезона прочитать нельзя. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; подтверждены British Automotive Winter, даты 24 Sep–1 Oct, 14 активностей, порядок и все 7 Daily, включая Time Attack 30 Sep. |
| `forza_news` | no_current_item: официальный News индекс доступен; публикации текущей недели по Winter Playlist нет. |
| `forza_support_release_notes` | unavailable: секция Release Notes вернула Internal Error; обновление текущей недели подтвердить нельзя. |
| `forza_support_known_issues` | unavailable: настроенная Known Issues страница вернула Internal Error; свежий официальный список проблем не прочитан. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум Forza; новой публикации Playlist на этой неделе не найдено. |
| `reddit_forzahorizon` | checked: проверены лента и свежий Winter Breakdown от 24 Sep; новых подтверждённых решений/изменений условий не обнаружено. |
| `reddit_forzahorizon6` | checked: проверены лента и Winter Playlist Guide от 24 Sep; новые условия/коды не выявлены. Зафиксировано неофициальное предупреждение об ANNA Autopilot для чистого круга Monthly Rivals. |
| `reddit_forza` | checked: проверена лента и Winter Information Thread Series 5 от 24 Sep; подтверждены сезонный порядок, награды и Daily. |
| `reddit_forzatune` | no_current_item: проверена лента и поиск текущей недели; свежих FH6/Winter тюнингов за 24–30 Sep не найдено, старые коды не переносились. |
| `forza_horizon_hub` | unavailable: сайт вернул Internal Error при живом открытии; актуальные данные сезона не использованы. |
| `forza_labs_collector` | unavailable: Collector Tool вернул Internal Error; свежую collectible-разметку подтвердить нельзя. |
| `forza_labs_map` | no_current_item: Interactive Map открыта, но сезонной Playlist-разметки/новых точных локаций Winter не содержит. |
| `escorenews_fh6` | checked: индекс временно вернул Internal Error, но поиск подтвердил свежие статьи от 24 Sep по #BambooPerfect, Shimanoyama Treasure Hunt и Winter Rallies Trial; новых уточнений сверх уже внесённых в карточки не найдено. |
| `dungg_playlist` | unavailable: YouTube playlist вернула Internal Error; выпуск текущей недели подтвердить нельзя. |

## 2026-09-29T15:52:00+07:00 — ручное изменение графика аудитории

- Пользователь попросил ограничить публичный график динамики посещаемости последними семью днями. Просмотрен живой официальный Playlist: Series 5 `British Automotive — Winter`, активен 24 сентября — 1 октября 2026; дедлайн прежний `2026-10-01T21:30:00+07:00`, сезон не менялся.
- Для проверки актуальности карточек просмотрены свежие текущенедельные материалы Reddit и Escorenews. Новых подтверждённых изменений карточек/решений для внесения не выявлено. Этот запуск меняет только отображаемый диапазон графика; исходная полная история метрик остаётся без изменений.
- Повторная проверка всех 14 визуальных записей: 13 отдельных подготовленных игровых плиток и их исходные пользовательские скриншоты на месте; SHA-256 подготовленных плиток сверены и зарегистрированы в audit.json. В online-источниках более точных отдельных плиток этой недели не найдено. Daily остаётся намеренно текстовым, без публичного визуала/запроса скриншота. `automation/audit_visual_evidence.ps1`: `VISUAL_QUEUE_STATUS=READY`.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: FH6 Series category недоступна через live fetch; старые сведения и изображения не использовались. |
| `fandom_current` | unavailable: Fandom вернул HTTP 402; сезонную страницу и игровые плитки прочитать нельзя. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; подтверждены Series 5 Winter и её период 24 сентября — 1 октября. |
| `forza_news` | no_current_item: официальный индекс доступен, новой публикации текущей недели не обнаружено; материал от 7 сентября не считался свежим. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes вернула Internal Error; свежую заметку недели подтвердить нельзя. |
| `forza_support_known_issues` | no_current_item: список открыт; видимая официальная запись обновлена 20 июля, связанных с текущей Playlist исправлений этой недели не обнаружено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую страницу Forza Forums; свежего объявления Playlist не найдено. |
| `reddit_forzahorizon` | checked: просмотрен текущенедельный Winter breakdown от 24 сентября и сезонный tuning guide от 25 сентября; новых подтверждённых изменений карточек нет. |
| `reddit_forzahorizon6` | checked: проверены Winter Playlist guide от 24 сентября и tuning guide от 25 сентября; новых подтверждённых изменений карточек нет. |
| `reddit_forza` | checked: проверены Winter Information Thread от 24 сентября и текущий tuning guide; новых подтверждённых изменений карточек нет. |
| `reddit_forzatune` | no_current_item: текущая лента проверена; свежей публикации FH6/Winter за текущую неделю не обнаружено. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но сезонной записи Series 5 Winter текущей недели не содержит. |
| `forza_labs_collector` | unavailable: Collector Tool не удалось загрузить через live fetch; новых collectible-фактов не подтверждено. |
| `forza_labs_map` | no_current_item: Interactive Map доступна как общая карта, актуальной Playlist-разметки или точной плитки Winter не содержит. |
| `escorenews_fh6` | checked: найдены и просмотрены свежие статьи от 24 сентября по #BambooPerfect, Treasure Hunt и Winter Rallies Trial; они не меняют факты текущих карточек. |
| `dungg_playlist` | unavailable: YouTube playlist не загрузилась через live fetch; свежий выпуск недели подтвердить нельзя. |

## 2026-10-01T06:19:43+07:00 — повторная проверка Steam и активной недели

- Live Playlist и официальный анонс подтверждают, что Series 5 Winter продолжается до 1 октября 14:30 UTC (21:30 Красноярск); страница Playlist уже заранее показывает Spring (1–8 октября), поэтому Spring не подставлялся в активные карточки до игрового сброса. Проверены все 16 настроенных источников.
- Повторно проверены все 14 визуальных записей активной Winter: 13 отдельных сезонных плиток с исходными пользовательскими доказательствами, Daily оставлен намеренно текстовым. Новых более точных актуальных плиток в доступных свежих источниках не найдено. Статусы visual: confirmed=0, community=13, preliminary=0, missing=1 (Daily intentionally text-only; no screenshot requested).
- Steam RU и EN: локальные тексты сгенерированы по текущему Winter state (3738 и 3352 символа, оба ниже лимита 4800). Обновлены только существующие секции 9235220 и 9330926. Публичная страница в браузере подтверждает обе локали и коды; Steam checker после подтверждения показывает UPDATE_REQUIRED из-за несовпадений своей публичной HTML-сверки (часть tune/condition полей и единственная ссылка GitHub в описании не обнаруживаются автоматическим fetch). Отпечатки записаны лишь после публичной проверки; финальный checker не UP_TO_DATE, причина остаётся открытой.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: категория Fandom недоступна live; данные и визуалы оттуда не использовались. |
| `fandom_current` | unavailable: текущая FH6 страница Fandom не открывается; сезонные решения/плитки не использовались. |
| `forza_playlist` | checked: официальная Playlist открыта. Текущая по расписанию Winter заканчивается 1 Oct в 14:30 UTC; страница уже предварительно показывает Spring 1–8 Oct. Spring карточки не приняты до времени сброса. Winter conditions и порядок сверены с опубликованной таблицей. |
| `forza_news` | no_current_item: официальный индекс доступен; свежего анонса/решений именно для Winter недели за последние дни нет. Серия 5 анонс от 7 Sep — контекст, не свежий weekly материал. |
| `forza_support_release_notes` | no_current_item: секция недоступна прямому чтению; связанная release note от 7 Sep известна, обновления текущей недели не обнаружены. |
| `forza_support_known_issues` | no_current_item: официальная Known Issues страница доступна; последняя видимая правка 20 Jul, актуального Winter playlist issue нет. |
| `forza_forums_official` | no_current_item: официальный форум сообщает о закрытии прежних форумов и переходе к Forza News/Feedback Portal; свежей playlist-публикации нет. |
| `reddit_forzahorizon` | checked: проверена лента и закреплённый Series 5 материал; релевантный новый текущенедельный пост по Winter решениям не найден. |
| `reddit_forzahorizon6` | checked: проверена текущая лента; свежего Spring материала нет, Winter решений сверх внесённых не обнаружено. |
| `reddit_forza` | checked: найден Winter Information Thread от 24 Sep; подтверждает смену на Spring 1 Oct в 14:30 UTC, новых условий Winter сверх Playlist нет. |
| `reddit_forzatune` | no_current_item: лента доступна, свежей публикации по текущей FH6 Winter неделе/тюнингу не найдено. |
| `forza_horizon_hub` | checked: сайт открыт; свежей разметки/гайда по текущей Winter неделе, карт или точных игровых плиток не обнаружено. |
| `forza_labs_collector` | checked: Collector Tool открыт; сезонной Playlist коллекционной активности на текущей неделе не содержит. |
| `forza_labs_map` | checked: Interactive Map открыта; общая карта, точных плиток Festival Playlist не содержит. |
| `escorenews_fh6` | no_current_item: FH6 индекс недоступен прямому чтению; поиск не выявил более свежих Winter решений, пригодных для внесения. Старые/следующие недели не перенесены. |
| `dungg_playlist` | unavailable: YouTube playlist недоступна live; выпуск текущей Winter недели подтвердить нельзя. |

## 2026-10-02T06:12:04+07:00 — rollover и полный аудит Series 5 Spring

- Живая официальная Playlist подтверждает Series 5 `British Automotive — Spring`, 1–8 октября; расписание Spring Information Thread указывает следующий сброс 8 октября 14:30 UTC (21:30 Красноярск). Официальная таблица и два свежих Reddit-материала совпадают по порядку, ограничениям, наградам и полному списку семи Daily. В state внесены 14 активностей; Monthly Rivals добавлен последним согласно порядку гайда.
- Подтверждены текущие Spring условия Weekly, Photo #TempleVantage, Treasure Hunt, Rally on Dirt, Aston Martin Nights, Drift Attack, Clifftop Crest Danger Sign, Ine Beach Speed Trap, Trial Hyper Sprints, три Horizon Play и Monthly Rivals. В свежем r/ForzaHorizon6 опубликованы актуальные коды для чемпионатов/PR/Trial; они внесены без имён авторов. Точное положение Nangan chest остаётся открытым: свежий пост показывает image spoiler, но текстовая локация не подтверждена, требуется проверить сам Photo Clue/карту.
- Проведён отдельный поиск Spring игровых плиток по официальной Playlist/News, текущим Reddit-гайдам и поиску изображений; результаты поиска показывают старые и обзорные визуалы, но не точные Spring плитки по каждой активности. Ничего из Winter не перенесено. Визуалы: `confirmed=0, community=0, preliminary=0, missing=14` (13 отдельных плиток запрошены, Daily остаётся намеренно текстовым без запроса изображения). `automation/audit_visual_evidence.ps1` должен сформировать очередь 13 полных скриншотов.
- Открытые поля: визуалы 13 карточек кроме Daily; точное решение Treasure Hunt Nangan. Отдельные tune-коды включены только там, где они есть в свежем текущенедельном Spring-гайде. Неизвестные сведения не заполнены предположениями.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: категория Fandom открыта live, но возвращает Internal Error; сезонные факты и визуалы оттуда не использовались. |
| `fandom_current` | unavailable: актуальная Fandom Series 5 страница возвращает Internal Error; старые статьи не использовались. |
| `forza_playlist` | checked: https://forza.net/fh6playlists открыта; строки 426–446 подтверждают Spring, 14 активностей, награды, классы, маршруты и требования; Spring 1–8 Oct. |
| `forza_news` | no_current_item: официальный индекс просмотрен, новой отдельной Series 5 Spring новости текущей недели нет. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes вернула Internal Error; в Known Issues index последняя опубликованная release note — Sep 7, новой за текущую неделю не найдено. |
| `forza_support_known_issues` | checked: официальная страница открыта; последнее обновление 20 Jul, актуального Spring Playlist issue среди видимых записей нет; страница направляет в Feedback Portal за текущим issue status. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую Forza Forums; отдельного свежего Spring Playlist объявления не обнаружено. |
| `reddit_forzahorizon` | checked: открыт breakdown Series 5 Spring от 1 Oct; сверены Weekly, все Daily, Photo и Treasure facts, новые уточнения не конфликтуют с официальной Playlist. |
| `reddit_forzahorizon6` | checked: открыт новый Series 5 Spring guide от 1 Oct; сверены маршруты, ограничения, reward cars и share codes; актуальные изображения — игровые/локационные иллюстрации, не полные точные плитки. |
| `reddit_forza` | checked: открыта Spring Information Thread Series 5 от 1 Oct и Spring breakdown; подтверждены даты, 7 Daily, сезонные reward thresholds и Monthly Rivals. |
| `reddit_forzatune` | no_current_item: текущая лента и поиск свежей недели проверены; отдельного FH6 Series 5 Spring tuning-поста в r/ForzaTune не найдено; настройки из прошлых сезонов не переносились. |
| `forza_horizon_hub` | checked: сайт открыт, но его weekly Playlist section всё ещё сообщает Series 1; эти данные явно устарели и не использовались для Spring. |
| `forza_labs_collector` | checked: Collector Tool открыт; сезонных Spring collectibles текущей недели не показывает, поэтому не добавлялся отдельный Collectibles card. |
| `forza_labs_map` | checked: Interactive Map открыта; свежей Spring Playlist разметки/точных игровых плиток нет. |
| `escorenews_fh6` | no_current_item: FH6 индекс и поиск проверены; текущей Spring Series 5 статьи нет, найденные статьи относятся к прошлым сериям. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist URL проверен, но live fetch вернул Internal Error; публикацию текущего Spring выпуска подтвердить не удалось. | 

## 2026-10-03T01:20:00+07:00 — повторная регистрация аудита Series 5 Spring после исправления Daily text-only проверки

- Guarded попытка `fh6-20261002-231146-202478` не опубликовала отчёт: предсезонный preflight ошибочно считал намеренно текстовый Daily карточкой с потерянным визуалом. Валидатор, audit guard и preflight теперь согласованы с правилом `not_applicable` для Daily; прошлый запуск завершён `BLOCKED`, Home Assistant получил CheckBlocked. Текущий запуск повторяет полный цикл; дата в сводке не обновлялась.
- Свежая повторная сверка подтвердила активный Series 5 `British Automotive — Spring`, дедлайн 08.10.2026 21:30 Красноярск и официальный порядок семи Daily. Снова проверены все обязательные live источники. В state уже записаны 12 точных плиток из пользовательских скриншотов; Daily оставлен без публичного изображения. Monthly Rivals карточка сохранена, но его плитки в новых изображениях нет; визуал и решение Treasure Hunt Nangan остаются открытыми.
- Счётчики visual: `confirmed=12`, `community=0`, `preliminary=0`, `missing=1` (Monthly Rivals), `not_applicable=1` (Daily). Полные исходные скриншоты и точные неизменённые вырезки сохранены в `reports/assets/series-05-spring/user-tiles-20261002/`.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live категория Fandom снова вернула Internal Error; старые данные не использованы. |
| `fandom_current` | unavailable: текущая страница Fandom Series/Season вернула Internal Error; прежние страницы не использованы. |
| `forza_playlist` | checked: официальная Playlist открыта повторно; строки 426–446 подтверждают Spring activities и Daily order, строка 360 — Monthly Rivals. |
| `forza_news` | no_current_item: официальный индекс доступен; отдельной новости Series 5 Spring на текущей неделе нет. |
| `forza_support_release_notes` | unavailable: настроенный Release Notes section вернул Internal Error. |
| `forza_support_known_issues` | checked: Known Issues доступна, последние видимые записи старые; текущенедельного playlist issue нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправлен на общую Forza Forums; актуального объявления не найдено. |
| `reddit_forzahorizon` | checked: текущий Spring breakdown доступен; его порядок двух Daily расходится с официальной таблицей. Оставлен официальный порядок. |
| `reddit_forzahorizon6` | checked: актуальный FH6-specific Spring guide доступен и подтверждает карточки, условия и коды недели. |
| `reddit_forza` | checked: Spring Information Thread и недельная tune thread доступны; проверены условия, reward cars, Daily и Monthly Rivals. |
| `reddit_forzatune` | no_current_item: live `/new` лента доступна, поста FH6 Series 5 Spring за эту неделю нет. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но weekly блок всё ещё указывает Series 1 и не годится как источник актуального Spring. |
| `forza_labs_collector` | unavailable: повторный live reader вернул Internal Error; актуальную сезонную collectible-информацию подтвердить нельзя. |
| `forza_labs_map` | checked: Interactive Map доступна; точная позиция Nangan chest/current playlist overlay не подтверждена. |
| `escorenews_fh6` | unavailable: индекс вернул Internal Error; актуальный Spring guide не подтверждён. |
| `dungg_playlist` | unavailable: YouTube playlist вернула Internal Error; видео текущей недели подтвердить нельзя. |

## 2026-10-03T00:27:00+07:00 — повторный аудит и пользовательские игровые плитки Series 5 Spring

- Активный сезон повторно подтверждён live: Series 5 `British Automotive — Spring`, действует до 08.10.2026 21:30 Asia/Krasnoyarsk. Официальная Playlist (строки 426–446) подтверждает сезонные награды, Weekly, полный порядок Daily, Photo, Treasure, два чемпионата, PR, Trial и Horizon Play; Monthly Rivals проверен в строке 360. Свежая Spring Information Thread r/forza подтверждает сроки, содержание заданий и ежемесячную гонку.
- Из присланных пользователем трёх изображений сохранены оригиналы `source-1.png`–`source-3.png`; без ретуши вырезаны ровно 12 актуальных игровых плиток в `reports/assets/series-05-spring/user-tiles-20261002/`. Кадры проверены визуально. В `data/current-season.json` внесены соответствующие `visual.image`, оригинальный `visual.sourceImage`, ориентация и происхождение. Daily намеренно оставлен текстовым, без публичного изображения. Monthly Rivals есть в карточках, но его плитки среди переданных кадров нет — визуал остаётся открытым.
- Статусы визуалов (14 карточек state): `confirmed=12`, `community=0`, `preliminary=0`, `missing=1` (Monthly Rivals), `not_applicable=1` (Daily, текстовая сводка). Закрыты 12 запросов точных плиток и ошибочный запрос визуала для Daily. Открыты только визуал Monthly Rivals и текстовое решение для точной позиции сундука Nangan.
- В живых Reddit-источниках найдено расхождение порядка Daily: один breakdown r/ForzaHorizon переставляет Drift Skills и Aftermarket Car, тогда как официальная Playlist, Spring Information Thread r/forza, FH6-specific guide r/ForzaHorizon6 и полученный игровой экран подтверждают текущий порядок в state; оставлен приоритетный официальный/FH6 порядок без изменения карточки. В свежем Community tune thread замечено сообщение автора об отсутствии новых tune-рекомендаций на этой неделе; уже подтверждённые значения не заменялись.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live категория Fandom возвращает Internal Error; не использовалась для фактов и изображений. |
| `fandom_current` | unavailable: страницы текущей Series/Season Fandom возвращают Internal Error; старые данные не переносились. |
| `forza_playlist` | checked: официальная таблица открыта; текущая Spring и все активности подтверждены на строках 426–446; Monthly Rivals Series 5 — строка 360. |
| `forza_news` | no_current_item: официальный индекс доступен, отдельной свежей Series 5 Spring новости за текущую неделю не найдено. |
| `forza_support_release_notes` | unavailable: Release Notes section вернула Internal Error; свежей релизной заметки недели не подтверждено. |
| `forza_support_known_issues` | checked: Known Issues доступна; видимое обновление от 20 Jul 2026, Playlist-багов Spring не указано; актуальный список направляет в Feedback Portal. |
| `forza_forums_official` | no_current_item: тег перенаправлен на общую страницу Forza Forums; текущей официальной playlist-публикации нет. |
| `reddit_forzahorizon` | checked: breakdown Series 5 Spring от 01 Oct прочитан; выявлен конфликт порядка двух Daily против официального источника, поэтому сохранён порядок официальной таблицы и FH6 guide. |
| `reddit_forzahorizon6` | checked: свежий Spring guide от 01 Oct сверён; подтверждает даты, семь Daily, условия, награды и сезонные решения. |
| `reddit_forza` | checked: Spring Information Thread от 01 Oct и текущий tuning thread просмотрены; подтверждены даты, Daily, события, награды и Monthly Rivals. |
| `reddit_forzatune` | no_current_item: лента `new` открыта, актуального FH6 Spring материала недели не найдено; новые share codes не перенесены. |
| `forza_horizon_hub` | no_current_item: сайт доступен, однако блок «this week» сообщает Series 1; устаревшая Playlist не использована. |
| `forza_labs_collector` | checked: Collector Tool доступен; Spring collectibles карточку текущей недели не подтверждает. |
| `forza_labs_map` | checked: Interactive Map доступна, но отдельная актуальная Spring метка/позиция сундука Nangan не подтверждена. |
| `escorenews_fh6` | unavailable: FH6 индекс не открылся через live reader; свежая Spring статья не подтверждена. |
| `dungg_playlist` | unavailable: текущий playlist URL вернул Internal Error; выпуск этой недели подтвердить нельзя. |

## 2026-10-03T01:50:00+07:00 — повторный live-аудит после исправления text-only Daily во всех сборочных проверках

- Серия и Spring повторно подтверждены официальной Festival Playlist; дедлайн 08.10.2026 21:30 Красноярск. Все 16 обязательных источников перепроверены в этом запуске. Проверочные цепочки guard, season validator, artifact renderer и portable verifier согласованы: Daily допустимо иметь `visual=not_applicable`, пустые пути и не запрашивать публичную плитку.
- Тесты после исправлений: `automation/test_refresh_guard.py` — 27 passed; `automation/test_portable_report.py` — 21 passed, portable provider `fh6-portable/1.0.0`, в тестовом окружении `PORTABLE_VALIDATION=passed`, `PORTABLE_PACKAGE=passed`. Ранее два защищённых запуска остановились до публикации на обнаруженном несоответствии Daily; текущий полный цикл повторяется с исправленной проверкой.
- Визуалы остались без изменений: `confirmed=12`, `community=0`, `preliminary=0`, `missing=1` (визуал Monthly Rivals не прислан), `not_applicable=1` (Daily). Точная позиция Nangan Treasure остаётся единственным другим содержательным openItem.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: live категория Fandom вернула Internal Error. |
| `fandom_current` | unavailable: текущая страница Series/Season Fandom вернула Internal Error. |
| `forza_playlist` | checked: Live Playlist подтверждает Spring, текущие активности, семь Daily и Monthly Rivals Series 5. |
| `forza_news` | no_current_item: официальный индекс доступен; отдельной свежей Spring playlist новости нет. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes вернула Internal Error. |
| `forza_support_known_issues` | checked: Known Issues доступна; актуального playlist issue среди опубликованных проблем не видно. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет к общей странице форумов; свежего playlist сообщения нет. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown проверен; Daily order расходится с официальной таблицей, в state оставлен официальный порядок. |
| `reddit_forzahorizon6` | checked: свежий FH6-specific guide проверен; подтверждает текущую неделю, задания и решения. |
| `reddit_forza` | checked: текущая Information Thread и Spring tune thread проверены; подтверждены сроки и активности. |
| `reddit_forzatune` | no_current_item: свежей публикации FH6 текущей недели в `/new` нет. |
| `forza_horizon_hub` | no_current_item: доступный weekly-блок указывает Series 1 и не подтверждает текущую неделю. |
| `forza_labs_collector` | checked: Collector Tool доступен, текущей Spring collectible-активности не показывает. |
| `forza_labs_map` | checked: Interactive Map доступна, точная позиция Nangan Treasure не подтверждена. |
| `escorenews_fh6` | unavailable: FH6 category index вернул Internal Error. |
| `dungg_playlist` | unavailable: YouTube playlist вернула Internal Error; текущий выпуск не подтверждён. |

## 2026-10-03T06:07:00+07:00 — полный аудит Series 5 Spring

- Live-Playlist подтверждает Series 5 `British Automotive — Spring`, 1–8 октября; дедлайн состояния — 08.10.2026 21:30 Asia/Krasnoyarsk. Проверены все семь Daily и полный порядок активностей; карточное содержимое сверено с официальной таблицей и свежими публикациями недели.
- Новое подтверждённое уточнение: сундук Nangan находится в Irokawa Space Centre у Irokawa Circuit, на верхней бетонной площадке слева от ракеты, над дорогой. GamesHedge и Traxion опубликовали независимые пошаговые разборы 1 октября, а свежие разборы Reddit содержат ссылку/скриншот спойлера. Формулировка добавлена в RU/EN state с уровнем `community`; решение исключено из `missingFields` и `openItems`.
- Все 12 подготовленных пользовательских Spring-плиток повторно осмотрены: содержимое, названия, кадрирование и соответствие активности правильные. Daily намеренно текстовый. Итого визуалов: `confirmed=12`, `community=0`, `preliminary=0`, `missing=1` (Monthly Rivals), `not_applicable=1` (Daily). Нужен только один скриншот Monthly Rivals; прежние кадры не переиспользуются.

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: категория FH6 Fandom недоступна через live reader (Internal Error); архивные сведения не использовались. |
| `fandom_current` | unavailable: текущая Series/Season страница Fandom недоступна (402/Internal Error); старые страницы не использовались. |
| `forza_playlist` | checked: официальная таблица открыта; строки 426–446 подтверждают Spring, 14 активностей и порядок, строка 360 — Monthly Rivals. |
| `forza_news` | no_current_item: индекс доступен; Series 5 announcement опубликован раньше текущей недели, отдельной новой Spring новости нет. |
| `forza_support_release_notes` | unavailable: обязательный Support Release Notes endpoint вернул Internal Error; более ранняя заметка Series 5 не выдавалась за свежую. |
| `forza_support_known_issues` | checked: FH6 Known Issues открыта; свежей записи об ошибке Playlist Spring не обнаружено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум; свежего объявления текущей недели не найдено. |
| `reddit_forzahorizon` | checked: разбор Spring от 1 Oct подтверждает условия и точные дни Daily; его спойлер подтверждает сундук в Nangan. |
| `reddit_forzahorizon6` | checked: FH6-гайд от 1 Oct подтверждает сезон, ежедневные задания, машины, классы, коды и текущие решения; спойлер-ссылка осмотрена. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct подтверждает дедлайн, Daily, условия активностей и Monthly Rivals. |
| `reddit_forzatune` | no_current_item: проверена лента новых публикаций; актуального отдельного FH6 Spring тюнинг-поста не найдено, старые коды не переносились. |
| `forza_horizon_hub` | checked: FH6 Hub и доступные сведения о текущей Series просмотрены; полезной новой детали Spring сверх подтверждённых источников нет. |
| `forza_labs_collector` | checked: Collector Tool открыт; отдельной Spring Collectibles-активности в официальном списке нет. |
| `forza_labs_map` | checked: Interactive Map открыта; Nangan сундук не подтверждался по её маркеру, точную позицию взяли из двух свежих текстовых разборов. |
| `escorenews_fh6` | unavailable: FH6 раздел Escorenews вернул Internal Error; свежий недельный материал подтвердить не удалось. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist не открылся в live reader; выпуск текущей недели подтвердить нельзя. |

Дополнительная проверка открытого решения (вне `requiredSources`): [GamesHedge](https://www.gameshedge.com/forza-horizon-6-nangan-region-british-automotive-treasure-hunt-guide/) и [Traxion](https://traxion.gg/how-to-complete-the-series-5-week-4-nangan-region-treasure-hunt-in-forza-horizon-6/) — свежие публикации 1 октября с совпадающей локацией у ракеты в Irokawa Space Centre. Текст помечен как подтверждённый сообществом, а не официально проверенный в игре.

## 2026-10-03T10:23:00+07:00 — восстановление плитки Monthly Rivals

- Обновлена только `activity_14_monthly_rivals`; Weekly и объединённый Daily не менялись. Spring и предыдущая Winter-неделя относятся к одному месячному событию Series 5: Shimanoyama Sprint на 2025 McLaren W1.
- Проверены [официальная Playlist](https://forza.net/fh6playlists), [свежий Spring-разбор r/ForzaHorizon](https://www.reddit.com/r/ForzaHorizon/comments/1wuzhi5/fh6_series_5_spring_breakdown_and_rewards/) и [страница Winter с изображением Monthly Rivals](https://forzahorizonwiki.com/wiki/forza-horizon-6/series-5/winter-season/). Официальная Playlist и текущий разбор подтверждают актуальность события; онлайн-изображение [Wiki](https://wikiassets.net/forza-567d92/images/f8f4337a6d4c5efb94b5850083c7bfe9.webp) подтверждает саму плитку, но не завершение. Среди просмотренных веб-результатов не найден кадр этой активности одновременно с отметкой выполнения и без золотого эффекта.
- Плитка с видимой отметкой `COMPLETE` восстановлена из уже сохранённого пользовательского скриншота предыдущей недели того же Monthly Rivals. Исходный скриншот сохранён как evidence; подготовленная плитка и исходник скопированы побайтно в Spring assets. SHA-256 совпали с оригиналами (`8EA10C7C…D8E295F` для плитки и `1B2D21BF…EF62EB` для исходника). Золотой эффект присутствует в самой игре на завершённой плитке; он не удалялся и изображение не ретушировалось.
- `activity_14_monthly_rivals.visual` теперь `confirmed`; его visual `missingFields`/`openItems` закрыты. Число visual: `confirmed=13`, `community=0`, `preliminary=0`, `missing=0`, `not_applicable=1` (Daily остаётся текстовым).

Повторный live-аудит обязательных источников этого запуска:

| Источник | Результат |
|---|---|
| `fandom_series_category` | unavailable: текущая категория Fandom недоступна через live reader; не использовалась. |
| `fandom_current` | unavailable: Fandom недоступен через live reader; сезонные изображения из кэша не выдавались за свежие. |
| `forza_playlist` | checked: открытая официальная Playlist подтверждает Series 5 British Automotive — Spring (1–8 Oct); таблица содержит Monthly Rivals Shimanoyama Sprint. |
| `forza_news` | no_current_item: индекс Forza News доступен, совпадений по Spring нет; отдельной свежей новости недели не обнаружено. |
| `forza_support_release_notes` | unavailable: настроенная секция Release Notes вернула Internal Error. |
| `forza_support_known_issues` | checked: страница FH6 Known Issues доступна; записи про Monthly Rivals нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум, свежего объявления недели нет. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown подтверждает Shimanoyama Sprint и требование clean lap; отдельной плитки COMPLETE без золотого эффекта в посте нет. |
| `reddit_forzahorizon6` | checked: свежий FH6 Spring guide подтверждает месячное задание, Shimanoyama Sprint и 2025 McLaren W1; отдельной альтернативной COMPLETE-плитки нет. |
| `reddit_forza` | checked: Spring Information Thread подтверждает один clean lap на серию и награду Super Wheelspin; визуала требуемого вида не содержит. |
| `reddit_forzatune` | no_current_item: лента `/new` доступна, свежей FH6 Spring-публикации с Monthly Rivals плиткой нет. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но текущую Spring плитку Monthly Rivals не публикует. |
| `forza_labs_collector` | checked: Collector Tool доступен; Monthly Rivals не является collectible и новых сведений не даёт. |
| `forza_labs_map` | checked: Interactive Map доступна, но не содержит плитку Monthly Rivals или индикатор её выполнения. |
| `escorenews_fh6` | unavailable: FH6-раздел вернул Internal Error; свежий пригодный кадр подтвердить нельзя. |
| `dungg_playlist` | unavailable: YouTube playlist не открылась через live reader; выпуск недели и требуемое изображение подтвердить нельзя. |

## 2026-10-04T06:12:00+07:00 — полный ежедневный аудит Series 5 Spring

- Живая [официальная Festival Playlist](https://forza.net/fh6playlists) подтверждает **Series 5 British Automotive — Spring**, активную 1–8 октября; дедлайн — **08.10.2026 21:30 Asia/Krasnoyarsk**. Строки 426–446 подтверждают недельное задание, все семь типов Daily, Photo Challenge, Treasure Hunt, оба чемпионата, три PR Stunts, Trial и Horizon Play; строка 360 подтверждает Monthly Rivals **Shimanoyama Sprint / 2025 McLaren W1** на уровне Series. Свежие r/ForzaHorizon6 и r/forza Spring guides подтверждают условия и дату-соответствие всех семи Daily, награды и активности. В одном свежем посте r/ForzaHorizon перепутан порядок Daily (Aftermarket Car и Drift Skills); оставлен последовательный порядок, совпадающий с датированным FH6-гайдом и игровой очередью Playlist.
- Все подготовленные игровые плитки проверены повторно и сопоставлены с текущими активностями; исходники пользователя сохранены. Итог: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1** (объединённый Daily намеренно текстовый). Monthly Rivals остался привязан к тому же активному месячному событию и изображение не удалялось при смене недели. Дополнительный поиск точной completed-плитки Monthly Rivals без золотого свечения результатов не дал: доступны обычная плитка без статуса и ранее присланный завершённый кадр с игровым золотым состоянием. Неизвестную альтернативу и ретушь не использовал; текущая точная плитка оставлена.

| Источник | Результат проверки 06:12 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: live reader вернул Internal Error; категорию и её изображения не использовал. |
| `fandom_current` | unavailable: Fandom root также вернул Internal Error; старые сезонные сведения не переносил. |
| `forza_playlist` | checked: текущая официальная таблица подтверждает Series 5 Spring, срок до 8 Oct, все сезонные карточки и месячный Shimanoyama Sprint; семь Daily сведены в одну карточку отчёта. |
| `forza_news` | no_current_item: официальный индекс доступен; свежей отдельной Spring Playlist новости за неделю не найдено. |
| `forza_support_release_notes` | unavailable: настроенный раздел Support вернул Internal Error; свежую заметку не подтверждал. |
| `forza_support_known_issues` | checked: страница Known Issues открылась; упоминания Playlist Spring/Monthly Rivals в доступном тексте не найдено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общий Forza Forums; текущего официального поста Playlist не обнаружено. |
| `reddit_forzahorizon` | checked: breakdown Spring от 1 Oct подтверждает сезонные условия/наград и Monthly Rivals; его распределение Daily по дням расходится с более точным FH6-гайдом. |
| `reddit_forzahorizon6` | checked: свежий FH6-гайд от 1 Oct проверен; подтверждает даты Oct 1–7 для всех Daily, Weekly/Photo/Treasure, события, маршруты, классы, награды и рекомендации. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct подтверждает дедлайн 8 Oct 14:30 UTC, порядок условий Daily, Photo/Treasure и месячный clean lap. |
| `reddit_forzatune` | no_current_item: лента `/new` проверена; свежего FH6 Spring-тюнинг-поста за эту неделю не найдено, share codes не переносились из старых публикаций. |
| `forza_horizon_hub` | no_current_item: открытая страница показывает Series 1, поэтому как источник текущей Spring не использовалась. |
| `forza_labs_collector` | checked: Collector Tool доступен; активности Collectibles в подтверждённой текущей Playlist нет. |
| `forza_labs_map` | checked: актуальная карта доступна, но не публикует сезонные плитки/завершённое Monthly Rivals; новых локационных фактов не добавлял. |
| `escorenews_fh6` | unavailable: FH6 landing page вернула Internal Error; свежего недельного гайда или подходящей плитки не подтверждено. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist вернул Internal Error; видео недели подтвердить нельзя. |

## 2026-10-05T06:08:00+07:00 — полный ежедневный аудит Series 5 Spring

- Живая официальная Playlist по-прежнему подтверждает **Series 5 British Automotive — Spring**, активную до **08.10.2026 21:30 Asia/Krasnoyarsk**. Проверены недельные активности, награды, семь Daily и месячная **Shimanoyama Sprint / 2025 McLaren W1**. Свежие текущенедельные обсуждения r/ForzaHorizon6 и r/forza сверены; в r/ForzaHorizon обнаружено расхождение в распределении двух Daily, поэтому сохраняется порядок, совпадающий с официальной Playlist и FH6-гайдом.
- Для полного списка Daily подтверждены даты 1–7 октября: Trading Paint Skills; Road Race; Drift/E-Drift Skills; покупка Aftermarket Car; звезда Horizon Rush; звезда Danger Signs; круг Drift Attack.
- Повторно проверены все подготовленные индивидуальные плитки и исходники. Итого визуалов: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1** (объединённый Daily намеренно текстовый). Очередь `audit_visual_evidence.ps1`: `READY`, 14 карточек проверено, `screenshotsRequired=0`. Октябрьская плитка Monthly Rivals сохранена без изменений: тот же Shimanoyama Sprint остаётся активен в этом месяце; файл не удалялся и повторно не запрашивался.
- Содержательных изменений карточек и `openItems` не найдено. Требуется только обычное обновление времени полной проверки и публикация производных отчётов.

| Источник | Результат проверки 06:08 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: live категория Fandom вернула Internal Error; сезонные данные из кэша не использовались. |
| `fandom_current` | unavailable: текущая Fandom Series/Season страница вернула Internal Error; изображения оттуда не переносились. |
| `forza_playlist` | checked: официальная Playlist подтверждает Series 5 Spring, период 1–8 Oct, все сезонные активности, семь Daily и Monthly Rivals Shimanoyama Sprint. |
| `forza_news` | no_current_item: официальный индекс проверен; отдельной свежей Spring Playlist новости текущей недели не обнаружено. |
| `forza_support_release_notes` | unavailable: настроенный раздел Release Notes вернул Internal Error. |
| `forza_support_known_issues` | checked: FH6 Known Issues просмотрен; свежего Playlist/Monthly Rivals issue в доступном материале нет. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общую страницу форумов; свежего объявления текущей недели не найдено. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown проверен; условия сверены, но публикация расходится в порядке двух Daily. |
| `reddit_forzahorizon6` | checked: свежий FH6 Spring guide проверен; подтверждает активную неделю, активности и полный список Daily. |
| `reddit_forza` | checked: текущая Spring Information Thread проверена; подтверждает дедлайн, условия недели и последовательность Daily. |
| `reddit_forzatune` | no_current_item: лента новых публикаций проверена; отдельного свежего FH6 Spring tuning-поста нет, старые коды не использовались. |
| `forza_horizon_hub` | no_current_item: сайт проверен, но доступный weekly-блок показывает Series 1 и не подтверждает текущую Spring-неделю. |
| `forza_labs_collector` | checked: Collector Tool доступен; отдельной сезонной collectible-активности в Playlist нет. |
| `forza_labs_map` | checked: Interactive Map доступна; подтверждённых новых локационных фактов этой проверки нет. |
| `escorenews_fh6` | unavailable: FH6-раздел вернул Internal Error; свежего недельного материала подтвердить не удалось. |
| `dungg_playlist` | unavailable: YouTube playlist не открылась через live reader; выпуск текущей недели подтвердить нельзя. |

## 2026-10-07T08:43:00+07:00 — внеплановый аудит Series 5 Spring

- Официальная Festival Playlist продолжает показывать **Series 5 British Automotive — Spring** до **08.10.2026 21:30 Asia/Krasnoyarsk**. Текущую неделю не переключал на анонсированную заранее Series 6; новый плейлист стартует только в момент официального сброса.
- Свежий FH6 Spring guide подтверждает полный список семи Daily: 1 Oct Trading Paint Skills; 2 Oct Road Race; 3 Oct Drift/E-Drift Skills; 4 Oct Aftermarket Car; 5 Oct Horizon Rush; 6 Oct Danger Signs; 7 Oct Drift Attack. Отдельный r/ForzaHorizon breakdown расходится в порядке нескольких заданий; сохранён порядок, совпадающий с официальной таблицей и FH6-specific guide. Для Horizon Rush гайд уточняет, что засчитываются Pier Pressure, Launch Control или Off Piste; это было советом к уже истёкшему заданию 5 Oct, поэтому текущую карточку не менял.
- Официальные **Horizon Meets / Release Notes от 5 Oct** объявляют исправление эксплуатации набора очков Drift Attack fast travel/rewind, но оно действует с 8 Oct, в момент следующего сезонного сброса. До этого момента текущий Drift Attack остаётся согласно опубликованным условиям; изменений карточек до вступления фикса не требуется. Известных ошибок текущих Spring-условий на Known Issues странице не обнаружено.
- Все 14 карточек проверены визуально повторно: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1** (Daily намеренно текстовый). Все подготовленные плитки и исходники на месте и SHA-256 совпадают; очередь `audit_visual_evidence.ps1` — `READY`, `screenshotsRequired=0`. Октябрьская плитка Monthly Rivals Shimanoyama Sprint сохранена без изменения: это та же ежемесячная активность, повторный скриншот не запрашивался.
- Содержательных изменений state и открытых пунктов нет; выполнить штатное обновление метки полной проверки и пересобрать публикацию.

| Источник | Результат проверки 08:43 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: live категория Forza Wiki/Fandom вернула Internal Error; кэш не использовался. |
| `fandom_current` | unavailable: Fandom root/текущая Series page вернула Internal Error; плитки оттуда не брались. |
| `forza_playlist` | checked: живая таблица подтверждает Series 5 Spring, даты, все текущие события и Daily; новая Series 6 ещё не активна. |
| `forza_news` | checked: опубликованы официальные Release Notes Horizon Meets от 5 Oct с новыми возможностями и датой следующего плейлиста 8 Oct; Spring-условия пока не изменены. |
| `forza_support_release_notes` | checked: исходная секция Release Notes не открылась; найден и просмотрен текущий официальный FH6 Release Notes: October 5, 2026. Исправление Drift Attack включается 8 Oct. |
| `forza_support_known_issues` | checked: FH6 Known Issues доступна; активной записи, меняющей текущие Spring-условия, нет; страница ссылается на Release Notes Oct 5. |
| `forza_forums_official` | no_current_item: официальный тег перенаправляет на общий форум; свежего текущенедельного объявления не найдено. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown от 1 Oct и текущие результаты проверены; есть расхождение порядка Daily против официальной таблицы. |
| `reddit_forzahorizon6` | checked: FH6-specific Spring guide от 1 Oct подтверждает условия, все 7 дат Daily, маршруты, ограничения и советы; опубликованы уточнения по Horizon Rush. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct подтверждает дедлайн 8 Oct 14:30 UTC и контекст недели. |
| `reddit_forzatune` | no_current_item: `/new` проверена; актуальной отдельной FH6 Spring tune-публикации нет; старые share codes не переносились. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но его weekly-блок всё ещё указывает Series 1 и непригоден для подтверждения текущей Spring. |
| `forza_labs_collector` | unavailable: Collector Tool URL вернул Internal Error при открытии; текущая Playlist не содержит отдельной Collectibles activity. |
| `forza_labs_map` | checked: Interactive Map открывается, но свежих точных плиток/новых локационных данных для текущих карточек не обнаружено. |
| `escorenews_fh6` | unavailable: FH6-раздел вернул Internal Error; материал текущей недели недоступен. |
| `dungg_playlist` | unavailable: YouTube playlist вернула Internal Error; выпуск текущей недели подтвердить не удалось. |

## 2026-10-07T08:49:00+07:00 — полный аудит ежедневного запуска

- Повторная живая проверка подтверждает **Series 5 British Automotive — Spring** до **08.10.2026 21:30 Asia/Krasnoyarsk**; Series 6 и Horizon Meets описаны только как предстоящий сброс 8 октября, поэтому rollover не выполнялся. Условия, награды, текущие 7 Daily и порядок карточек остаются как в официальной Playlist.
- Официальный анонс/Release Notes от 5 октября проверен повторно: исправление эксплойта Drift Attack вступает в силу с 8 октября; текущую активную карточку это не меняет. Текущие обсуждения r/ForzaHorizon и FH6-guides учтены; отдельный Winter/Summer материал не переносился. Новых содержательных изменений для карточек, тюнингов, изображений и `openItems` не найдено.
- Повторная проверка всех визуалов: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1** (Daily текстовый). Подготовленные PNG и источники на месте, SHA совпадает; `audit_visual_evidence.ps1` — `READY`, 0 запросов скриншотов. Октябрьский Monthly Rivals tile оставлен без изменений.
- Сводка актуальна — содержательных изменений не требуется; обновляется только время полной проверки.

| Источник | Результат проверки 08:49 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: Fandom Series category вернула Internal Error; кэш не использован. |
| `fandom_current` | unavailable: текущий Fandom root/Series page вернул Internal Error; изображения не использованы. |
| `forza_playlist` | checked: открыта живая Playlist, Spring и весь набор активностей подтверждены до 8 Oct; следующий сезон ещё не активен. |
| `forza_news` | checked: официальный индекс проверен; найден свежий Horizon Meets/Release Notes анонс от 5 Oct с датой следующего сброса. |
| `forza_support_release_notes` | unavailable: Support endpoint и прямой Release Notes article вернули Internal Error в этом проходе; содержание официального анонса News сверено, недоступность endpoint зафиксирована. |
| `forza_support_known_issues` | checked: Known Issues доступна; нет известной активной проблемы, меняющей текущую Spring Playlist. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общую страницу форумов; текущего объявления Playlist не найдено. |
| `reddit_forzahorizon` | checked: текущий Spring breakdown от 1 Oct проверен; его порядок части Daily расходится с официальной таблицей. |
| `reddit_forzahorizon6` | checked: актуальный FH6-specific Spring guide подтверждает даты Daily и текущие условия; отдельного более нового seasonal guide нет. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct актуален для недели и подтверждает дедлайн 8 Oct 14:30 UTC. |
| `reddit_forzatune` | no_current_item: лента `/new` проверена; нового FH6 Spring tune post не найдено; старые коды не брались. |
| `forza_horizon_hub` | no_current_item: доступная weekly-панель по-прежнему показывает Series 1, поэтому не подтверждает активную Spring. |
| `forza_labs_collector` | checked: Collector Tool доступен; в текущей Playlist нет отдельного collectible задания. |
| `forza_labs_map` | checked: карта открывается; отдельной новой локационной информации для текущих карточек не найдено. |
| `escorenews_fh6` | unavailable: FH6 landing section вернула Internal Error; текущенедельная статья недоступна. |
| `dungg_playlist` | unavailable: configured YouTube playlist вернула Internal Error; выпуск недели подтвердить нельзя. |

## 2026-10-07T09:28:10+07:00 — повторная живая проверка перед повторной попыткой публикации

- Официальная Festival Playlist повторно подтверждает **Series 5 British Automotive — Spring** до **08.10.2026 21:30 Asia/Krasnoyarsk**. Horizon Meets/Series 6 уже объявлены официально, но стартуют только 8 октября; Thursday rollover сейчас не выполнялся.
- Сверил все 14 текущих активностей и полный список семи Daily. Официальная таблица совпадает с сохранённым порядком условий; один свежий breakdown r/ForzaHorizon переставляет Drift Skills и Aftermarket Car относительно официальной последовательности, поэтому его порядок не переношу. Свежий FH6-гайд и Information Thread подтверждают Spring и дедлайн. Условия не менялись.
- Официальный анонс Horizon Meets от 5 октября сообщает о фиксах, в том числе эксплойта набора очков Drift Attack, с релизом нового плейлиста 8 октября. Это не меняет ещё активную сегодня карточку.
- Повторно проверены все визуалы: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1** (Daily остаётся намеренно текстовым). Все 13 PNG-плиток и исходники пользователя присутствуют; подготовленные SHA-256 сверены. Октябрьский Monthly Rivals Shimanoyama Sprint сохранён вместе с исходником без изменений, поскольку активность та же. `audit_visual_evidence.ps1`: `READY`, 0 запросов скриншотов.
- **Сводка актуальна — содержательных изменений не требуется.** Повторная попытка предназначена только для публикационной проверки и итоговой доставки; открытых пунктов нет.

| Источник | Результат проверки 09:28 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: категория Forza Wiki/Fandom вернула Internal Error; данные и визуалы из кэша не использовались. |
| `fandom_current` | unavailable: текущая Series/Season страница Forza Wiki/Fandom вернула Internal Error; сезон подтверждён официальной Playlist. |
| `forza_playlist` | checked: живая таблица подтверждает Series 5 Spring, даты 1–8 Oct, активные события, Daily и ежемесячный Soni Circuit Monthly Rivals; Spring остаётся текущей до 8 Oct. |
| `forza_news` | checked: официальный индекс и Horizon Meets announcement от 5 Oct проверены; новые награды/Playlist начнутся 8 Oct. |
| `forza_support_release_notes` | unavailable: Support section и прямой Oct 5 article вернули Internal Error; доступное официальное Forza News summary подтверждает исправление Drift Attack, вступающее с 8 Oct. |
| `forza_support_known_issues` | checked: актуальная FH6 Known Issues страница открылась; текущего пункта, меняющего условия Spring, не обнаружено. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общий Forza Forums; поиск текущей Playlist/Series announcement не дал публикации этой недели. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown от 1 Oct проверен; условия совпадают, но последовательность двух Daily расходится с официальной таблицей. |
| `reddit_forzahorizon6` | checked: FH6-specific Spring guide и tune thread от 1 Oct проверены; подтверждают сезон и активности; текущие коды не требовалось менять. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct подтверждает смену плейлиста 8 Oct 14:30 UTC; отдельная Release Notes-публикация Forza Support от 5 Oct также просмотрена. |
| `reddit_forzatune` | no_current_item: `/new` проверена, поиском свежая FH6 публикация текущей недели не найдена; старые tune codes не переносились. |
| `forza_horizon_hub` | no_current_item: FH6 Hub доступен, но не показывает подтверждение актуальной Series 5 Spring; сезонный источник не использовался. |
| `forza_labs_collector` | checked: Collector Tool доступен; отдельной Collectibles activity в текущей Playlist нет. |
| `forza_labs_map` | checked: Interactive Map доступна; новых подтверждённых локаций или точных недельных плиток не публикует. |
| `escorenews_fh6` | unavailable: FH6 landing page вернула Internal Error; статью текущей недели проверить не удалось. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist вернул Internal Error; выпуск текущей недели подтвердить не удалось. |

## 2026-10-08T06:03:00+07:00 — повторная полная проверка Series 5 Spring перед вечерним rollover

- Живая официальная Festival Playlist подтверждает **Series 5 British Automotive — Spring (1–8 октября)** и её текущие карточки. Официальная новость Horizon Meets от 5 октября сообщает, что новые награды Playlist стартуют **8 октября**, поэтому на время проверки до **21:30 Asia/Krasnoyarsk** сохраняется Spring; Series 6 не активировал преждевременно.
- Условия и порядок сверены по текущей официальной таблице. Свежий r/ForzaHorizon breakdown и FH6 Spring guide от 1 октября относятся к действующей неделе; при расхождении последовательности Daily приоритет оставлен официальной таблице. В новом официальном патче от 5 октября указан фикс набора очков Drift Attack при fast travel/rewind, начинающий действовать с обновлением 8 октября; он не меняет текущую карточку до сброса.
- Все 14 activity визуалов проверены: **confirmed=13, community=0, preliminary=0, missing=0, not_applicable=1**. Daily остаётся текстовым по правилу проекта; 13 точных пользовательских плиток и исходники сохранены, хеши совпали. Октябрьская Monthly Rivals Shimanoyama Sprint сохранена без изменений в пределах того же месяца; повторный запрос изображения не нужен. `audit_visual_evidence.ps1` вернул `READY`, очередь скриншотов пуста.
- Новых подтверждённых изменений карточек или `openItems` нет. Полная проверка пройдена, требуется обновить метку проверки и выполнить защищённую публикацию.

| Источник | Результат проверки 06:03 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: live Fandom category вернула Internal Error; кэш не использовался. |
| `fandom_current` | unavailable: текущая Fandom Series/Season страница вернула Internal Error; плитки оттуда не переносились. |
| `forza_playlist` | checked: открыта текущая официальная таблица, подтверждает Series 5 Spring, даты 1–8 Oct, набор событий и Monthly Rivals; сезон заканчивается в 21:30 +07. |
| `forza_news` | checked: официальный анонс Horizon Meets от 5 Oct сообщает о новом Playlist с 8 Oct; до старта действующая Spring не заменена. |
| `forza_support_release_notes` | checked: раздел/статья Support прямым чтением вернула Internal Error, но официальный Forza News release notes от 5 Oct прочитан; фикс Drift Attack включается 8 Oct. |
| `forza_support_known_issues` | checked: живая Known Issues страница открылась; не выявлено записи, меняющей условия активной Spring. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общий форум; отдельного текущенедельного объявления Playlist не найдено. |
| `reddit_forzahorizon` | checked: свежий Spring breakdown от 1 Oct проверен; использован только как перекрёстная проверка, официальный порядок имеет приоритет. |
| `reddit_forzahorizon6` | checked: свежий FH6-specific Spring guide от 1 Oct подтверждает активности/даты; новый пост о будущей Series 6 не переносился в карточки Spring. |
| `reddit_forza` | checked: Spring Information Thread от 1 Oct подтверждает дедлайн 8 Oct 14:30 UTC; отдельный пост Release Notes от 5 Oct сверён с официальным анонсом. |
| `reddit_forzatune` | no_current_item: `/new` и поиск проверены; актуального нового FH6 Spring тюнинга не найдено, старые коды не переиспользованы. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но weekly-раздел не подтверждает активную Series 5 Spring; данные не использованы. |
| `forza_labs_collector` | checked: Collector Tool доступен; отдельной Collectibles активности в текущей Playlist нет. |
| `forza_labs_map` | checked: Interactive Map доступна; новых подтверждённых текущенедельных локационных фактов нет. |
| `escorenews_fh6` | unavailable: FH6-раздел вернул Internal Error; свежий материал этой недели подтвердить нельзя. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist вернул Internal Error; выпуск текущей недели подтвердить нельзя. |

## 2026-10-09T06:05:00+07:00 — полный аудит после живого rollover на Series 6 Summer

- Живая официальная Playlist и Forza News подтверждают новый активный сезон **Series 6 “Horizon Meets” — Summer**, 08.10.2026 21:30 — 15.10.2026 21:30 Asia/Krasnoyarsk. Официальная таблица задаёт порядок событий; свежие текущенедельные Reddit-гайды использованы как перекрёстная проверка и для маршрутов/тюнингов, не как замена официального условия.
- Подтверждены 13 карточек (Daily содержит 7 заданий). Weekly: 1973 BMW Turbo 2002, главы Speed Skills / Hokubu Time Attack / Speed Traps; Photo #LightLunch у 7-Eleven на любом Eclectic Domestic; Treasure Hunt Ito Region; чемпионаты Bee Happy, Ghost Hunter, Vetting the Competition; Soni Time Attack, Highway Jump, Konbini Dash; Trial Aim for the Top; Horizon Play Smooth and Steady; Monthly Rivals Daikoku Circuit на 2025 BMW M4 CS. Сундук не локализован: свежий гайд ссылается на картинку-спойлер, независимого подтверждения координат нет, поэтому точное место оставлено открытым.
- Октябрьская Monthly Rivals теперь **Daikoku Circuit**, не прежний Shimanoyama Sprint. Старую плитку и прежнее состояние не переносил: фактическая активность изменилась, нужен новый кадр.
- Визуально проверены все 13 активностей отдельно: **confirmed=0, community=0, preliminary=0, missing=12, not_applicable=1** (Daily намеренно без визуала). В актуальных официальных страницах и проверенных свежих текущенедельных постах не нашёл полных точных игровых плиток; сезонные инфографики/обзорные изображения не подставлялись. Открыты запросы исходных полных скриншотов по 12 визуальным карточкам, включая новую Monthly Rivals.

| Источник | Результат проверки 06:05 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: живая категория Forza Wiki/Fandom вернула Internal Error; кэш и старые визуалы не использованы. |
| `fandom_current` | unavailable: текущая Fandom Series/Season страница недоступна; сезон подтверждён официальными Playlist и News. |
| `forza_playlist` | checked: живая таблица подтверждает Series 6 Horizon Meets — Summer, даты 8–15 Oct +07, 13 активностей, условия, порядок, награды и новую Daikoku Circuit Monthly Rivals. |
| `forza_news` | checked: официальный анонс Horizon Meets от 5 Oct и текущий Playlist подтверждают старт новой серии 8 Oct; 7-Eleven Evolving World и новые награды сверены. |
| `forza_support_release_notes` | checked: Support release notes Oct 5 доступны по прямой статье; обновление Series 6 подтверждено, особого изменения условий карточек не найдено. |
| `forza_support_known_issues` | checked: текущая FH6 Known Issues страница открыта; пункта, меняющего условия Series 6, не найдено. |
| `forza_forums_official` | no_current_item: официальный тег/форум проверен, свежего подтверждения конкретного плейлиста этой недели не найдено; приоритет у официальной Playlist. |
| `reddit_forzahorizon` | checked: свежий Series 6 Summer breakdown от 8 Oct просмотрен; используется для сопоставления карточек/награды, не для замены источника условий. |
| `reddit_forzahorizon6` | checked: свежий Series 6 Summer guide от 8 Oct проверен; даёт главы, Daily, PR-условия, чемпионаты и tune codes. Treasure image-спойлер просмотрен как единственный источник и не считается независимым подтверждением координат. |
| `reddit_forza` | checked: свежая Series 6 Summer Information Thread от 8 Oct подтверждает даты/полный Daily; официальный дедлайн остаётся определяющим. |
| `reddit_forzatune` | no_current_item: свежая лента сообщества проверена; отдельной публикации FH6 Series 6 с тюнингами не обнаружено, неподтверждённые старые коды не переносились. |
| `forza_horizon_hub` | no_current_item: Hub проверен; точных плиток и подтверждённого специфичного решения для карточек Series 6 не найдено. |
| `forza_labs_collector` | unavailable: Collector Tool endpoint вернул Internal Error; в Playlist отдельной Collectibles activity нет. |
| `forza_labs_map` | checked: Interactive Map просмотрена; точную недельную плитку/доказательство сундука не даёт, координаты не подменялись догадкой. |
| `escorenews_fh6` | unavailable: FH6 landing section вернула Internal Error; свежий недельный материал недоступен. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist не удалось проверить; свежий выпуск недели не подтверждён. |

## 2026-10-09T12:15:00+07:00 — внеплановое обновление скриншотов Series 6 Summer

- Живая [официальная Festival Playlist](https://forza.net/fh6playlists) подтверждает Series 6 «Horizon Meets» — Summer, 8–15 октября 2026; дедлайн **15.10.2026 21:30 Asia/Krasnoyarsk**. Сверены 13 карточек, включая 7 Daily, порядок активности, условия, награды и Monthly Rivals Daikoku Circuit. Официальная [новость Series 6](https://forza.net/news/forza-horizon-6-series-6) и [Release Notes от 5 октября](https://support.forza.net/hc/en-us/articles/55985143856531-FH6-Release-Notes-October-5-2026) проверены. Known Issues открыта; актуального пункта, меняющего эти условия, не обнаружено.
- Проверены все обязательные источники: свежие публикации в `r/ForzaHorizon`, `r/ForzaHorizon6` и `r/forza` подтверждают текущую неделю; свежего FH6-поста в `r/ForzaTune` не найдено. Forza Horizon Hub и обе ForzaLabs-страницы доступны, но не дают точных плиток этой недели. Fandom (категория и текущая страница), раздел Support Release Notes, Escorenews FH6 и плейлист DungG не дали пригодного свежего материала/не открылись; старые данные оттуда не переносились.
- Получены три пользовательских полных кадра: `reports/assets/series-06-summer/user-source-1.png` (SHA-256 `896c6e9289b47ab4d588f0da52fe81799d9f9aa7b774f8d47cca0edf76239ace`), `user-source-2.png` (`37e197b25c9b0b3b26d8e53234dea7abb7c88cd6aece983a00b6778797232ce4`) и `user-source-3.png` (`d42758f5a7fa783e19db3c412d5d981156673e69020c5fb7f7ad00a37cf5b994`). Оригиналы сохранены байт-в-байт. Из них без ретуши, затемнения и оверлеев вырезаны отдельные полные игровые плитки для Weekly, Photo, Treasure Hunt, Bee Happy, Ghost Hunter, Vetting the Competition, Soni Time Attack, Highway Jump, Konbini Dash, Trial, Horizon Play и Monthly Rivals; все кадры визуально проверены. Monthly Rivals теперь показывает новый Daikoku Circuit, не прежний Shimanoyama.
- В состоянии обновлены локальные `visual.image`/`visual.sourceImage` и статусы подтверждения для 12 карточек; Daily намеренно остаётся текстовым. **confirmed=12, community=0, preliminary=0, missing=0, not_applicable=1.** У Treasure Hunt решение о точном местоположении сундука всё ещё предварительное и остаётся в `openItems`; изображение плитки не считается доказательством координат.

| Источник | Результат проверки 12:15 +07:00 |
|---|---|
| `fandom_series_category` | unavailable: живая категория Forza Wiki/Fandom не открылась; старые факты и изображения не использованы. |
| `fandom_current` | unavailable: текущая Series/Season-страница недоступна; сезон подтверждён официальной Playlist. |
| `forza_playlist` | checked: живая официальная Playlist подтверждает Series 6 Summer, 13 активностей, порядок, требования, награды и Daikoku Circuit. |
| `forza_news` | checked: официальная новость Horizon Meets проверена; согласуется с текущей Series 6. |
| `forza_support_release_notes` | checked: прямая статья Release Notes от 5 октября открыта; изменения плейлиста сверены. |
| `forza_support_known_issues` | checked: живая FH6 Known Issues открыта; правки текущих условий не обнаружены. |
| `forza_forums_official` | no_current_item: официальный тег перенаправил на общую страницу форумов; отдельного текущенедельного объявления Playlist не найдено. |
| `reddit_forzahorizon` | checked: пост Series 6 Summer от 8 октября просмотрен, карточки и недельный список сверены. |
| `reddit_forzahorizon6` | checked: FH6 Summer guide от 8 октября просмотрен; карточки/рекомендации сверены, неофициальные советы не подменяют условия Playlist. |
| `reddit_forza` | checked: свежая Summer Information Thread от 8 октября просмотрена; даты и расписание подтверждены. |
| `reddit_forzatune` | no_current_item: свежей публикации FH6 Series 6 в текущей ленте/поиске не найдено; старые коды не использовались. |
| `forza_horizon_hub` | no_current_item: сайт доступен, но свежего точного недельного материала/плиток для этих карточек нет. |
| `forza_labs_collector` | checked: Collector Tool открыт; отдельной Collectibles activity в текущей Playlist нет. |
| `forza_labs_map` | checked: Interactive Map открыта; точные плитки пользовательские, координаты сундука не подтверждены картой. |
| `escorenews_fh6` | unavailable: FH6 landing page не открылась; свежая статья недели не подтверждена. |
| `dungg_playlist` | unavailable: настроенный YouTube playlist не открылся; выпуск недели не подтверждён. |
