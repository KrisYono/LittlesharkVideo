param(
    [Parameter(Mandatory=$true)]
    [string]$RemoteUrl
)

$git = Get-Command git -ErrorAction SilentlyContinue
if (-not $git) {
    Write-Error "Git is not installed or not available in PATH. Install Git first: https://git-scm.com/download/win"
    exit 1
}

if (-not (Test-Path ".git")) {
    git init
}

git add .
git commit -m "Initial little shark video project"
git branch -M main

$existingRemote = git remote get-url origin 2>$null
if ($LASTEXITCODE -eq 0) {
    git remote set-url origin $RemoteUrl
} else {
    git remote add origin $RemoteUrl
}

git push -u origin main
