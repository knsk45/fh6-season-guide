function Get-Fh6NotificationText {
    [CmdletBinding()]
    param(
        [Parameter(Mandatory=$true)][ValidateSet('UpdateRequired','UpToDate','CheckBlocked')][string]$Status,
        [object]$CheckedResult,
        [object]$Metrics
    )
    $Title='';$Lines=@()
    switch ($Status) {
        'UpToDate' {
            $Title='FH6 — всё актуально'
            if ($CheckedResult -and ([string]$CheckedResult.message).Contains('содержательных изменений не требуется')) {
                $Lines=@('Сайт и Steam актуальны.','Новых данных нет. Дата проверки обновлена.')
            } else { $Lines=@('Проверка завершена. Сайт и Steam актуальны.') }
        }
        'UpdateRequired' {
            $Title='FH6 — Steam ждёт обновления'
            $Lines=@('Сайт проверен. Тексты Steam требуют обновления.','Статус и дальнейшие действия — в панели.')
        }
        'CheckBlocked' {
            $Title='FH6 — проверка остановлена'
            $Lines=@('Обновление не завершено.','Причина и статус — в панели.')
        }
    }
    if ($Metrics) {
        if ($Metrics.baselineCreated -eq $true) { $Lines+='Статистика: первый замер.' }
        else {
            $Views='{0:+0;-0;0}' -f [long]$Metrics.steam.viewsAdded
            $Favorites='{0:+0;-0;0}' -f [long]$Metrics.steam.favoritesAdded
            $Site='{0:+0;-0;0}' -f [long]$Metrics.github.viewsAdded
            $Lines+="Просмотры: Steam $Views, сайт $Site · избранное $Favorites."
        }
    }
    return [pscustomobject]@{title=$Title;message=($Lines -join "`n")}
}
