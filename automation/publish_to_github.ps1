[CmdletBinding()]
param(
    [string]$CommitMessage = "Update FH6 current season"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "daily-season"
$Repository = "knsk45/fh6-season-guide"
$PagesUrl = "https://knsk45.github.io/fh6-season-guide/reports/current-week.html"
$PagesFallbackIps = @(
    "185.199.108.153",
    "185.199.109.153",
    "185.199.110.153",
    "185.199.111.153"
)
$GitHubCli = "C:\Program Files\GitHub CLI\gh.exe"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Validator = Join-Path $PSScriptRoot "validate_season.ps1"
$StatePath = Join-Path $RepoRoot "data\current-season.json"
$script:UsePagesFallback = $false

function Assert-NativeSuccess {
    param([string]$Operation)

    if ($LASTEXITCODE -ne 0) {
        throw "$Operation failed with exit code $LASTEXITCODE."
    }
}

function Invoke-PagesRequest {
    param(
        [Parameter(Mandatory = $true)][string]$Uri,
        [ValidateSet('GET','HEAD')][string]$Method = 'GET'
    )

    if (-not $script:UsePagesFallback) {
        try {
            return Invoke-WebRequest -UseBasicParsing -Uri $Uri -Method $Method -TimeoutSec 20
        }
        catch {
            $script:UsePagesFallback = $true
            Write-Host "Direct GitHub Pages request failed; using the verified fallback edge for this run."
        }
    }

    $Target = [Uri]$Uri
    $TempPath = Join-Path ([IO.Path]::GetTempPath()) ("fh6-pages-" + [Guid]::NewGuid().ToString('N') + '.tmp')
    try {
        foreach ($PagesFallbackIp in $PagesFallbackIps) {
            $CurlArgs = @(
                '-L', '--fail', '--silent', '--show-error', '--max-time', '30',
                '--resolve', "$($Target.Host):443:$PagesFallbackIp"
            )
            if ($Method -eq 'HEAD') { $CurlArgs += '-I' }
            $CurlArgs += @('-o', $TempPath, '-w', '%{http_code}', $Uri)
            $StatusText = (& curl.exe @CurlArgs | Select-Object -Last 1).Trim()
            if ($LASTEXITCODE -ne 0) {
                continue
            }
            $StatusCode = [int]$StatusText
            $Content = if ($Method -eq 'GET') { Get-Content -LiteralPath $TempPath -Raw -Encoding UTF8 } else { '' }
            $Length = if ($Method -eq 'GET') { (Get-Item -LiteralPath $TempPath).Length } else { 0 }
            return [pscustomobject]@{
                StatusCode = $StatusCode
                RawContentLength = $Length
                Content = $Content
            }
        }
        throw "Request GitHub Pages failed through every configured fallback edge."
    }
    finally {
        Remove-Item -LiteralPath $TempPath -Force -ErrorAction SilentlyContinue
    }
}

Push-Location $RepoRoot
try {
    $ActualRoot = (git rev-parse --show-toplevel).Trim()
    Assert-NativeSuccess "Resolve Git repository"
    if ([IO.Path]::GetFullPath($ActualRoot) -ne [IO.Path]::GetFullPath($RepoRoot)) {
        throw "Refusing to publish from unexpected repository: $ActualRoot"
    }

    $CurrentBranch = (git branch --show-current).Trim()
    Assert-NativeSuccess "Read current branch"
    if ($CurrentBranch -ne $ExpectedBranch) {
        throw "Expected branch '$ExpectedBranch', current branch is '$CurrentBranch'."
    }

    $ValidationOutput = & $Validator -StatePath $StatePath
    $ValidationSucceeded = $?
    $ValidationOutput | Write-Host
    if (-not $ValidationSucceeded) {
        throw "Validate FH6 season structure failed."
    }

    git fetch origin $ExpectedBranch --quiet
    Assert-NativeSuccess "Fetch origin/$ExpectedBranch"

    git merge-base --is-ancestor "origin/$ExpectedBranch" HEAD
    if ($LASTEXITCODE -ne 0) {
        throw "Local branch does not contain origin/$ExpectedBranch. Resolve the divergence before publishing."
    }

    $PublishPaths = @(
        ".gitignore",
        "AGENTS.md",
        ".agents/skills",
        "CURRENT_WEEK.md",
        "seasons",
        "data",
        "reports/SOURCE_NOTES.md",
        "reports/artifact.json",
        "reports/current-week.html",
        "reports/steam-guide-current.txt",
        "reports/build_artifact.ps1",
        "reports/enhance_portable_html.mjs",
        "reports/assets",
        "README.md",
        "index.html",
        "docs",
        ":(exclude)docs/steam-review-fh6.txt",
        "automation/refresh_guard.py",
        "automation/test_refresh_guard.py",
        "automation/ha_refresh_watchdog.ps1",
        "automation/publish_to_github.ps1",
        "automation/check_steam_guide.ps1",
        "automation/collect_publication_metrics.ps1",
        "automation/mark_steam_guide_published.ps1",
        "automation/send_home_assistant_notification.ps1",
        "automation/refresh_last_content_update.ps1",
        "automation/render_season_markdown.ps1",
        "automation/render_steam_guide.ps1",
        "automation/start_new_season.ps1",
        "automation/validate_season.ps1"
    )

    git add -- @PublishPaths
    Assert-NativeSuccess "Stage FH6 report files"

    git diff --cached --quiet
    $DiffExitCode = $LASTEXITCODE
    if ($DiffExitCode -eq 1) {
        git commit -m $CommitMessage
        Assert-NativeSuccess "Commit FH6 report files"
    }
    elseif ($DiffExitCode -ne 0) {
        throw "Inspect staged changes failed with exit code $DiffExitCode."
    }
    else {
        Write-Host "No report changes to commit. Verifying the existing publication."
    }

    git push origin "HEAD:$ExpectedBranch"
    Assert-NativeSuccess "Push origin/$ExpectedBranch"

    $LocalSha = (git rev-parse HEAD).Trim()
    Assert-NativeSuccess "Read local commit"
    $RemoteLine = @(git ls-remote origin "refs/heads/$ExpectedBranch") | Select-Object -First 1
    Assert-NativeSuccess "Read remote commit"
    if (-not $RemoteLine) {
        throw "origin/$ExpectedBranch was not found after push."
    }
    $RemoteSha = ($RemoteLine -split "\s+")[0]
    if ($LocalSha -ne $RemoteSha) {
        throw "Publication verification failed: local $LocalSha, remote $RemoteSha."
    }

    if (-not (Test-Path -LiteralPath $GitHubCli)) {
        throw "GitHub CLI was not found at '$GitHubCli'; Pages verification cannot run."
    }

    $Deadline = (Get-Date).AddMinutes(3)
    $PagesRun = $null
    do {
        $RunsJson = & $GitHubCli api "repos/$Repository/actions/runs?head_sha=$LocalSha&per_page=20"
        Assert-NativeSuccess "Read GitHub Actions runs"
        $PagesRun = (($RunsJson | ConvertFrom-Json).workflow_runs | Where-Object {
            $_.path -eq "dynamic/pages/pages-build-deployment" -and $_.head_sha -eq $LocalSha
        } | Select-Object -First 1)
        if ($PagesRun -and $PagesRun.status -eq "completed" -and $PagesRun.conclusion -eq "success") {
            break
        }
        if ($PagesRun -and $PagesRun.status -eq "completed" -and $PagesRun.conclusion -ne "success") {
            throw "GitHub Pages deployment failed for commit $LocalSha with conclusion '$($PagesRun.conclusion)'."
        }
        Start-Sleep -Seconds 5
    } while ((Get-Date) -lt $Deadline)

    if (-not $PagesRun -or $PagesRun.status -ne "completed" -or $PagesRun.conclusion -ne "success") {
        throw "GitHub Pages did not confirm deployment of commit $LocalSha within three minutes."
    }

    $Response = Invoke-PagesRequest -Uri $PagesUrl
    if ($Response.StatusCode -ne 200 -or $Response.RawContentLength -le 0) {
        throw "Published report check failed for $PagesUrl."
    }

    $PublishedHtml = [string]$Response.Content
    $State = Get-Content -LiteralPath $StatePath -Raw -Encoding UTF8 | ConvertFrom-Json
    $PublishedCards = ([regex]::Matches($PublishedHtml, 'data-activity-block')).Count
    if ($PublishedCards -ne [int]$State.season.expectedCardCount) {
        throw "Published report contains $PublishedCards cards; expected $($State.season.expectedCardCount)."
    }
    $AssetPaths = @([regex]::Matches($PublishedHtml, 'src="(assets/[^"]+)"') | ForEach-Object { $_.Groups[1].Value } | Sort-Object -Unique)
    foreach ($AssetPath in $AssetPaths) {
        $AssetUrl = [Uri]::new([Uri]$PagesUrl, $AssetPath).AbsoluteUri
        $AssetResponse = Invoke-PagesRequest -Uri $AssetUrl -Method HEAD
        if ($AssetResponse.StatusCode -ne 200) {
            throw "Published asset check failed: $AssetUrl"
        }
    }

    Write-Host "PUBLISHED_SHA=$LocalSha"
    Write-Host "PAGES_URL=$PagesUrl"
}
finally {
    Pop-Location
}
