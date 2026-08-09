[CmdletBinding()]
param(
    [string]$CommitMessage = "Update FH6 current season"
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$ExpectedBranch = "daily-season"
$Repository = "knsk45/fh6-season-guide"
$PagesUrl = "https://knsk45.github.io/fh6-season-guide/reports/current-week.html"
$GitHubCli = "C:\Program Files\GitHub CLI\gh.exe"
$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path

function Assert-NativeSuccess {
    param([string]$Operation)

    if ($LASTEXITCODE -ne 0) {
        throw "$Operation failed with exit code $LASTEXITCODE."
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

    git fetch origin $ExpectedBranch --quiet
    Assert-NativeSuccess "Fetch origin/$ExpectedBranch"

    git merge-base --is-ancestor "origin/$ExpectedBranch" HEAD
    if ($LASTEXITCODE -ne 0) {
        throw "Local branch does not contain origin/$ExpectedBranch. Resolve the divergence before publishing."
    }

    $PublishPaths = @(
        "CURRENT_WEEK.md",
        "seasons",
        "reports/SOURCE_NOTES.md",
        "reports/artifact.json",
        "reports/current-week.html",
        "README.md",
        "index.html",
        "automation/publish_to_github.ps1"
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

    $Response = Invoke-WebRequest -UseBasicParsing -Uri $PagesUrl -TimeoutSec 30
    if ($Response.StatusCode -ne 200 -or $Response.RawContentLength -le 0) {
        throw "Published report check failed for $PagesUrl."
    }

    Write-Host "PUBLISHED_SHA=$LocalSha"
    Write-Host "PAGES_URL=$PagesUrl"
}
finally {
    Pop-Location
}
