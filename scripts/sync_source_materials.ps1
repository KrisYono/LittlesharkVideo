param(
    [string]$SourceRoot,
    [string]$RepoRoot,
    [string]$CommitMessage = "Sync latest little shark materials"
)

$littleSharkFolder = -join ([char[]](
    0x5C0F, 0x9CA8, 0x9C7C, 0x5FB7, 0x5DDE, 0x79D1, 0x666E, 0x5C0F, 0x89C6, 0x9891
))
$defaultSourceRoot = Join-Path "C:\Users\Kawaii\OneDrive - Simon Fraser University (1sfu)\Desktop" $littleSharkFolder
$defaultRepoRoot = "C:\Users\Kawaii\OneDrive - Simon Fraser University (1sfu)\Desktop\Little_shark_video\LittlesharkVideo"

$ErrorActionPreference = "Stop"

if (-not $SourceRoot) {
    $SourceRoot = $defaultSourceRoot
}

if (-not $RepoRoot) {
    $RepoRoot = $defaultRepoRoot
}

function Get-GitPath {
    $git = Get-Command git -ErrorAction SilentlyContinue
    if ($git) {
        return $git.Source
    }

    $githubDesktopGit = Join-Path $env:LOCALAPPDATA "GitHubDesktop\app-3.5.12\resources\app\git\cmd\git.exe"
    if (Test-Path -LiteralPath $githubDesktopGit) {
        return $githubDesktopGit
    }

    throw "Git was not found in PATH or GitHub Desktop."
}

if (-not (Test-Path -LiteralPath $SourceRoot)) {
    throw "Source folder not found: $SourceRoot"
}

if (-not (Test-Path -LiteralPath $RepoRoot)) {
    throw "Repo folder not found: $RepoRoot"
}

$destinationRoot = Join-Path (Join-Path $RepoRoot "source_materials") $littleSharkFolder
New-Item -ItemType Directory -Force -Path $destinationRoot | Out-Null

$copied = 0
$sourceFiles = Get-ChildItem -Force -Recurse -LiteralPath $SourceRoot -File

foreach ($sourceFile in $sourceFiles) {
    $relativePath = $sourceFile.FullName.Substring($SourceRoot.Length).TrimStart("\")
    $destinationFile = Join-Path $destinationRoot $relativePath
    $needsCopy = $true

    if (Test-Path -LiteralPath $destinationFile) {
        $existing = Get-Item -LiteralPath $destinationFile
        $needsCopy = ($existing.Length -ne $sourceFile.Length)
    }

    if ($needsCopy) {
        New-Item -ItemType Directory -Force -Path (Split-Path -LiteralPath $destinationFile) | Out-Null
        Copy-Item -LiteralPath $sourceFile.FullName -Destination $destinationFile -Force
        $copied++
    }
}

$git = Get-GitPath
$status = & $git -C $RepoRoot status --short

if (-not $status) {
    Write-Output "No changes detected. Source files: $($sourceFiles.Count)."
    exit 0
}

& $git -C $RepoRoot add source_materials .gitattributes README.md scripts
& $git -C $RepoRoot commit -m $CommitMessage
& $git -C $RepoRoot push -u origin main

Write-Output "Synced $copied file(s), committed, and pushed to origin/main."
