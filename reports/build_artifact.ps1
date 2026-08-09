param(
    [string]$CountdownOverride
)

$ErrorActionPreference = 'Stop'
$projectRoot = Split-Path -Parent $PSScriptRoot
$assetRoot = Join-Path $PSScriptRoot 'assets\fandom-spring'
$artifactPath = Join-Path $PSScriptRoot 'artifact.json'
$generatedAt = [DateTimeOffset]::Now

function Get-AssetDataUri([string]$FileName) {
    $path = Join-Path $assetRoot $FileName
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing report asset: $path"
    }
    $extension = [IO.Path]::GetExtension($path).TrimStart('.').ToLowerInvariant()
    $mime = switch ($extension) {
        'jpg' { 'image/jpeg' }
        'jpeg' { 'image/jpeg' }
        'png' { 'image/png' }
        default { throw "Unsupported image type: $path" }
    }
    $base64 = [Convert]::ToBase64String([IO.File]::ReadAllBytes($path))
    return "data:$mime;base64,$base64"
}

$official = 'https://forza.net/fh6playlists'
$fandom = 'https://forza.fandom.com/wiki/Forza_Horizon_6/Series_3/Spring_Season'
$reddit = 'https://www.reddit.com/r/ForzaHorizon/comments/1vh4bio/fh6_series_3_spring_breakdown_and_rewards/'
$awes0me = 'https://www.reddit.com/r/ForzaHorizon/comments/1vh5knw/fh6_seasonal_tunes_by_awes0me_beau/'
$xiii90 = 'https://www.reddit.com/r/ForzaHorizon6/comments/1vh5x51/series_3_spring_seasonals_weekly_tunes_by_xiii90/'

$cards = @(
    [ordered]@{
        id = 'activity_01_weekly'; number = '01'; icon = '🚗'; kind = 'Weekly Challenge'; title = 'Racing Spirit'; points = '5 очков';
        condition = '1980 Abarth Fiat 131; суммарно 4 звезды на Trailblazers, 2 победы в Dirt Races и 3 Ultimate Wreckage Skills.';
        how = 'Повторяйте Coastal Descent, начиная примерно за 704 м по северо-восточной дороге. Если Abarth не допускается в обычную Dirt Race: пройденная гонка → Custom Race → Use My Car или Anything Goes.';
        tune = '1980 Abarth Fiat 131 — <b>Awes0me Beau</b>, <code>207 861 362</code>; запасной — <b>XIII90</b>, <code>996 668 231</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>тюнинг Awes0me Beau</a> · <a href='$xiii90'>тюнинг XIII90</a>"
    },
    [ordered]@{
        id = 'activity_02_daily'; number = '02'; icon = '📅'; kind = 'Daily Challenges'; title = 'Все 7 дней'; points = '7 × 1 очко';
        condition = @'
<ol class="days">
  <li><b>Чт — All the Colors:</b> 3 звезды за один проезд Rainbow Run Speed Trap, 140 mph / 225,3 км/ч. Ferrari 458 Italia S1 800 — <b>Awes0me Beau</b>, <code>796 821 422</code>.</li>
  <li><b>Пт — Stadium Scenery:</b> сфотографировать свою машину у Horizon Stadium. Подойдёт любой автомобиль; удобно взять Lamborghini Huracán EVO.</li>
  <li><b>Сб — Thunderbird 2:</b> 2 звезды на Thunderbird Drift Zone на итальянской машине. Ferrari Dino 246 GT S1 800 — <b>Awes0me Beau</b>, <code>518 222 242</code>.</li>
  <li><b>Вс — What’s It Gonna Be?:</b> использовать Wheelspin или Super Wheelspin; машина не нужна.</li>
  <li><b>Пн — Flinging Mud:</b> 5 Air Skills во время Dirt Races. Abarth Fiat 131 — <b>Awes0me Beau</b>, <code>207 861 362</code>.</li>
  <li><b>Вт — Taking the Reins:</b> Great Skill Chain на Lamborghini. Huracán EVO S1 800 — <b>Awes0me Beau</b>, <code>194 351 203</code>.</li>
  <li><b>Ср — Shopping Trip:</b> победить в Electric Town Circuit. Ferrari 488 GTB S1 800 — <b>Awes0me Beau</b>, <code>172 533 643</code>.</li>
</ol>
'@;
        how = 'Daily открываются по одному в 21:30 (Красноярск). Для Rainbow Run нужен один результат на 3 звезды; для Electric Town Circuit можно снизить сложность Drivatar.';
        tune = 'Авторы и коды указаны возле каждого дня; где автомобиль не влияет на зачёт, лишний тюнинг не предлагается.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$reddit'>условия по дням</a> · <a href='$awes0me'>тюнинги</a>"
    },
    [ordered]@{
        id = 'activity_03_photo'; number = '03'; icon = '📷'; kind = 'Photo Challenge'; title = '#SkiHoliday'; points = '2 очка';
        condition = 'Сфотографировать любую Lamborghini у Sotoyama Ski Resort; награда — эмоция Take Off.';
        how = 'Телепортируйтесь к Snow Forest Cross Country Circuit. Курорт находится непосредственно к юго-западу от значка гонки: <a href="https://forzahorizonhub.com/map?cat=landmark&amp;loc=568818">точная метка</a> · <a href="https://image.u4n.com/article/202605/sLpXhAaaDi8GbZNxbghE0fZPgmksBv8SXttgcWM8.webp">скриншот карты</a>.';
        tune = '2020 Lamborghini Huracán EVO S1 800 — <b>Awes0me Beau</b>, <code>194 351 203</code>. Для самого снимка тюнинг не обязателен.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$reddit'>ориентир сообщества</a>"
    },
    [ordered]@{
        id = 'activity_04_treasure'; number = '04'; icon = '🧰'; kind = 'Treasure Hunt'; title = 'Takashiro Region'; points = '3 очка';
        condition = 'Follow the Photo Clue to Discover the Treasure; награда — 100 000 CR.';
        how = 'Крайний запад Takashiro: каменистый берег реки у конца красной пунктирной грунтовки, напротив небольшой красной пагоды. <a href="https://preview.redd.it/q4bgddulsrhh1.jpeg?width=3840&amp;format=pjpg&amp;auto=webp&amp;s=db86d1695d2cd1c06b7791673588495893e3d5a1">общая карта</a> · <a href="https://preview.redd.it/4enbzoyomrhh1.jpg?width=4032&amp;format=pjpg&amp;auto=webp&amp;s=c7dfe005e53b6c26c07b0100cfa94b16d4ad43f1">точка крупно</a> · <a href="https://preview.redd.it/wj0n2oyomrhh1.jpg?width=4032&amp;format=pjpg&amp;auto=webp&amp;s=1b90b3585099f10506700f38b8e39d7fe31f6b3f">вид сундука</a>. Красная иконка иногда не появляется.';
        tune = 'Любой автомобиль; тюнинг не требуется.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='https://www.reddit.com/r/ForzaHorizon6/comments/1vh5z0b/100k_box_location/'>карта и сундук</a>"
    },
    [ordered]@{
        id = 'activity_05_loop'; number = '05'; icon = '🏁'; kind = 'Seasonal Championship'; title = 'Out of the Loop!'; points = '5 очков';
        condition = 'B600 Total Buggies &amp; Offroad, Dirt: Kawazu Nanadaru Scramble, Cherry Field Trail, Chiheisen Scramble. Награда — 2022 Maserati MC20.';
        how = 'Выиграйте чемпионат по сумме трёх гонок. Для поиска допустимых машин включите фильтры Buggies, Pickups &amp; 4x4s, Unlimited Buggies и Unlimited Offroad.';
        tune = '2019 Toyota 4Runner TRD Pro — <b>Awes0me Beau</b>, <code>171 532 374</code>; запасной 1997 Mitsubishi Montero Evolution — <b>XIII90</b>, <code>973 413 685</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>основной тюнинг</a> · <a href='$xiii90'>запасной тюнинг</a>"
    },
    [ordered]@{
        id = 'activity_06_snow'; number = '06'; icon = '❄️'; kind = 'Seasonal Championship'; title = 'It''s Snow Problem At All'; points = '5 очков';
        condition = 'A700 Sports Utility Heroes, Cross Country: Snow Forest Circuit, Tateyama Alpine, Soni Highlands. Награда — 2014 Lamborghini Huracán LP 610-4.';
        how = 'Держите ровный темп на снегу и берегите очки чемпионата; победа в каждом отдельном заезде не обязательна.';
        tune = '2015 Range Rover Sport SVR — <b>Awes0me Beau</b>, <code>913 262 787</code>. Запасные: Lamborghini Urus — <b>Awes0me Beau</b>, <code>101 588 982</code>; Porsche Cayenne — <b>XIII90</b>, <code>496 172 094</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>Awes0me Beau</a> · <a href='$xiii90'>XIII90</a>"
    },
    [ordered]@{
        id = 'activity_07_drag'; number = '07'; icon = '🚦'; kind = 'Drag Meet'; title = 'Festival Kilometer'; points = '3 очка';
        condition = 'Lamborghini S1 800, время не хуже 18,000 с; награда — Wheelspin.';
        how = 'Используйте открытый Drag Meet со значком стартовой «ёлки», а не обычную Festival Drag Race. Займите слот и дождитесь зелёного сигнала.';
        tune = '2020 Lamborghini Huracán EVO — <b>Awes0me Beau</b>, <code>194 351 203</code> (заявлено 17,150 с); запасной 2024 Temerario — <b>Awes0me Beau</b>, <code>126 461 876</code> (17,217 с).';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>автор и результаты</a>"
    },
    [ordered]@{
        id = 'activity_08_speed_trap'; number = '08'; icon = '⚡'; kind = 'Speed Trap'; title = 'Takashiro Bridge'; points = '2 очка';
        condition = 'Ferrari S1 800, 165 mph / 265,5 км/ч; награда — Wheelspin.';
        how = 'Разгоняйтесь с востока; у основного тюнинга есть запас до заявленных автором 183 mph / 294,5 км/ч.';
        tune = '2009 Ferrari 458 Italia — <b>Awes0me Beau</b>, <code>796 821 422</code>; запасной 2015 Ferrari 488 GTB — <b>Awes0me Beau</b>, <code>172 533 643</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>автор тюнингов</a>"
    },
    [ordered]@{
        id = 'activity_09_speed_zone'; number = '09'; icon = '🛣️'; kind = 'Speed Zone'; title = 'Kōzokudōro'; points = '2 очка';
        condition = 'Ferrari S1 800, средняя скорость 200 mph / 321,9 км/ч; награда — Wheelspin.';
        how = 'Начинайте примерно за 2,1 км с юго-запада и держите максимально плавную траекторию.';
        tune = '2015 Ferrari 488 GTB — <b>Awes0me Beau</b>, <code>172 533 643</code>; запасной Ferrari 458 Italia — <b>Awes0me Beau</b>, <code>796 821 422</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>автор тюнингов</a>"
    },
    [ordered]@{
        id = 'activity_10_drift'; number = '10'; icon = '💨'; kind = 'Drift Zone'; title = 'Nukabira Turn'; points = '2 очка';
        condition = 'Ferrari S1 800, 64 000 очков; награда — Wheelspin.';
        how = 'Входите с востока, удерживайте одну передачу и широкий угол. Отключите TCS/STM, если они режут пробуксовку.';
        tune = '1969 Ferrari Dino 246 GT — <b>Awes0me Beau</b>, <code>518 222 242</code>; запасной 2020 Ferrari Roma — <b>DCxReason</b>, <code>612 265 990</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>основной тюнинг</a>"
    },
    [ordered]@{
        id = 'activity_11_trial'; number = '11'; icon = '👥'; kind = 'The Trial'; title = 'Daily Commute'; points = '10 очков';
        condition = 'Alfa Romeo A700, Road: Ito Sprint, Tokyo Railway Sprint, Highway Circuit. Награда — 2020 Ferrari SF90 Stradale.';
        how = 'Не выталкивайте союзников, пропускайте более быстрых игроков и безопасно блокируйте Drivatar. Обычно достаточно выиграть две гонки из трёх.';
        tune = '2017 Alfa Romeo Giulia Quadrifoglio — <b>Awes0me Beau</b>, <code>141 394 828</code>; запасной 1992 Alfa Romeo 155 Q4 — <b>XIII90</b>, <code>172 625 950</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$awes0me'>Awes0me Beau</a> · <a href='$xiii90'>XIII90</a>"
    },
    [ordered]@{
        id = 'activity_12_spec'; number = '12'; icon = '🎮'; kind = 'Horizon Play / Spec Racing'; title = 'Up to Spec?'; points = '3 очка';
        condition = 'Завершить чемпионат Spec Racing; награда — 2007 Alfa Romeo 8C Competizione.';
        how = 'Войдите в доступный Spec Racing Championship и завершите все требуемые этапы.';
        tune = 'Машина и спецификация фиксируются событием; пользовательский share code не применяется.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$reddit'>состав недели</a>"
    },
    [ordered]@{
        id = 'activity_13_stunt'; number = '13'; icon = '🎉'; kind = 'Horizon Stunt Party'; title = 'Mini Games'; points = '3 очка';
        condition = 'Завершить любую Stunt Party; награда — клаксон Wah Wah Wah Wahhh.';
        how = 'Регистрация открывается в начале каждого часа примерно на 10 минут. Примите приглашение в свободной езде и доберитесь до старта.';
        tune = 'Подойдёт любой автомобиль. Универсальный вариант — 2020 Lamborghini Huracán EVO S1 800, <b>Awes0me Beau</b>, <code>194 351 203</code>.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$reddit'>расписание Stunt Party</a>"
    },
    [ordered]@{
        id = 'activity_14_rivals'; number = '14'; icon = '⏱️'; kind = 'Monthly Rivals'; title = 'Electric Town Circuit'; points = '1 очко в Spring';
        condition = 'Чистый круг на выданном 2024 Lamborghini Temerario; карточка показывает 4 очка Series и Super Wheelspin.';
        how = 'Проедьте спокойно, не касаясь стен и не используя перемотку. В Spring зачисляется 1 очко, остальные три распределены по другим сезонам Series 3.';
        tune = 'Фиксированный 2024 Lamborghini Temerario; пользовательский тюнинг не применяется.';
        source = "<a href='$official'>официальная Playlist</a> · <a href='$reddit'>условие Rivals</a>"
    }
)

$visuals = @{
    activity_01_weekly     = @{ image = 'FH6_Series3Spring.jpg';             icon = 'FH6_EventSeasonal_Drive_Icon.png';       position = '50% 18%' }
    activity_02_daily      = @{ image = 'FH6_Series3Spring.jpg';             icon = 'FH6_EventSeasonal_Stunt_Icon.png';       position = '50% 18%' }
    activity_03_photo      = @{ image = 'FH6_S3Spring_PhotoChallenge.jpg';   icon = 'FH6_EventFP_PhotoChallenge_Icon.png';    position = '50% 31%' }
    activity_04_treasure   = @{ image = 'FH6_S3Spring_TreasureHunt.jpg';     icon = 'FH6_EventFP_TreasureHunt_Icon.png';      position = '50% 28%' }
    activity_05_loop       = @{ image = 'FH6_S3Spring_Champ1.jpg';           icon = 'FH6_EventFP_DirtScramble_Icon.png';      position = '50% 50%' }
    activity_06_snow       = @{ image = 'FH6_S3Spring_Champ2.jpg';           icon = 'FH6_EventFP_CrossCountryCircuit_Icon.png'; position = '50% 50%' }
    activity_07_drag       = @{ image = 'FH6_S3Spring_HorizonLife.jpg';      icon = 'FH6_EventFP_DragMeet_Icon.png';          position = '50% 50%' }
    activity_08_speed_trap = @{ image = 'FH6_S3Spring_SpeedTrap.jpg';        icon = 'FH6_EventFP_SpeedTrap_Icon.png';         position = '50% 50%' }
    activity_09_speed_zone = @{ image = 'FH6_S3Spring_SpeedZone.jpg';        icon = 'FH6_EventFP_SpeedZone_Icon.png';         position = '50% 50%' }
    activity_10_drift      = @{ image = 'FH6_S3Spring_DriftZone.jpg';        icon = 'FH6_EventFP_DriftZone_Icon.png';         position = '50% 50%' }
    activity_11_trial      = @{ image = 'FH6_S3Spring_Trial.jpg';            icon = 'FH6_EventFP_Trial_Icon.png';             position = '50% 28%' }
    activity_12_spec       = @{ image = 'FH6_S3Spring_HorizonPlay.jpg';      icon = 'FH6_EventFP_HorizonPlay_Icon.png';       position = '50% 50%' }
    activity_13_stunt      = @{ image = 'FH6_S3Spring_HorizonLife.jpg';      icon = 'FH6_EventFP_StuntParty_Icon.png';        position = '50% 50%' }
    activity_14_rivals     = @{ image = 'FH6_S3_MonthlyRivals.jpg';          icon = 'FH6_EventFP_MonthlyRivals_Icon.png';     position = '50% 50%' }
}

function New-CardHtml([hashtable]$card) {
    $visual = $visuals[$card.id]
    if (-not $visual) { throw "No visual mapping for $($card.id)" }
    $cardImage = Get-AssetDataUri $visual.image
    $cardIcon = Get-AssetDataUri $visual.icon
    $imagePosition = $visual.position
    @"
<style>
  :root{color-scheme:dark}*{box-sizing:border-box}body{margin:0;background:#071014;color:#eef6f5;font-family:Inter,Segoe UI,Arial,sans-serif}.card{overflow:hidden;border:1px solid #29434b;border-radius:18px;background:linear-gradient(145deg,#111c21,#081014);box-shadow:0 18px 40px #0008}.wrap{display:grid;grid-template-columns:230px 1fr;gap:0}.visual{position:relative;width:190px;height:190px;align-self:start;margin:20px;background:#111;overflow:hidden;border-radius:14px}.visual>img{display:block;width:190px;height:190px;object-fit:cover;object-position:$imagePosition;filter:saturate(.96) contrast(1.04) brightness(.78)}.visual:after{content:'';position:absolute;inset:0;background:linear-gradient(180deg,transparent 38%,#061014dd)}.activity-icon{position:absolute;z-index:2;left:16px;top:16px;display:grid;place-items:center;width:56px;height:56px;border-radius:14px;background:#d9ff00;box-shadow:0 8px 24px #0008}.activity-icon img{width:42px;height:42px;object-fit:contain}.number{position:absolute;z-index:2;left:16px;bottom:14px;font-weight:900;font-size:36px;letter-spacing:-1px}.content{padding:20px 24px 20px 0}.eyebrow{display:flex;gap:10px;align-items:center;flex-wrap:wrap;color:#b8ccd1;font-size:12px;font-weight:800;text-transform:uppercase;letter-spacing:.08em}.points{border-radius:999px;background:#e4007f;color:white;padding:5px 9px;letter-spacing:0;text-transform:none}h2{margin:7px 0 13px;font-size:26px;line-height:1.05;color:#fff}p{margin:9px 0;line-height:1.48}.label{color:#d9ff00;font-weight:800}.tune{padding:10px 12px;border-left:3px solid #d9ff00;background:#0e2025;border-radius:0 9px 9px 0}code{white-space:nowrap;background:#1d3238;border:1px solid #36515a;border-radius:6px;padding:2px 6px;color:#fff}.sources{margin-top:14px;padding-top:10px;border-top:1px solid #29434b;color:#8ea8ae;font-size:12px}.sources a{color:#9fd7ff}.days{margin:8px 0;padding-left:20px}.days li{margin:7px 0;line-height:1.42}@media(max-width:650px){.wrap{grid-template-columns:1fr}.visual{width:170px;height:170px;margin:18px auto 0}.visual>img{width:170px;height:170px}.content{padding:18px}h2{font-size:23px}}
</style>
<article class="card">
  <div class="wrap">
    <div class="visual"><img src="$cardImage" alt="Игровая карточка $($card.title) из Series 3 Spring"><span class="activity-icon"><img src="$cardIcon" alt="Иконка $($card.kind)"></span><span class="number">$($card.number)</span></div>
    <div class="content">
      <div class="eyebrow"><span>$($card.kind)</span><span class="points">$($card.points)</span></div>
      <h2>$($card.title)</h2>
      <p><span class="label">Условие:</span> $($card.condition)</p>
      <p><span class="label">Как выполнить:</span> $($card.how)</p>
      <p class="tune"><span class="label">Автомобиль и тюнинг:</span> $($card.tune)</p>
      <div class="sources">$($card.source) · <a href='$fandom'>изображение и иконка: Forza Wiki</a></div>
    </div>
  </div>
</article>
"@
}

$blocks = for ($i = 0; $i -lt $cards.Count; $i++) {
    [ordered]@{
        id = $cards[$i].id
        type = 'html'
        layout = 'full'
        body = New-CardHtml -card $cards[$i]
    }
}

$artifact = [ordered]@{
    surface = 'dashboard'
    manifest = [ordered]@{
        version = 1
        surface = 'dashboard'
        title = 'Forza Horizon 6: Как пройти Series 3 "Italian Exotics" - Весна'
        description = "Сезон действует до четверга 21:30 по Красноярску"
        generatedAt = $generatedAt.ToString('o')
        blocks = $blocks
        charts = @()
        sources = @()
    }
    snapshot = [ordered]@{
        version = 1
        status = 'ready'
        generatedAt = $generatedAt.ToString('o')
        datasets = [ordered]@{}
        accessIssues = @()
    }
    sources = @()
    package_info = [ordered]@{
        generated_at = $generatedAt.ToString('o')
        workflow = 'weekly-fh6-complete-playlist-guide'
    }
}

$json = $artifact | ConvertTo-Json -Depth 100
[IO.File]::WriteAllText($artifactPath, $json, [Text.UTF8Encoding]::new($false))
Write-Output "Wrote $artifactPath with $($blocks.Count) activity blocks and per-activity Fandom visuals"
