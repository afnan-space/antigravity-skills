# One-Click Installer for Antigravity Custom Skills (Windows PowerShell)
$ErrorActionPreference = "Stop"

$TargetDir = Join-Path $HOME ".gemini\config\skills"
Write-Host ">>> Installing Antigravity Skills to: $TargetDir" -ForegroundColor Cyan

if (-not (Test-Path $TargetDir)) {
    New-Item -ItemType Directory -Path $TargetDir -Force | Out-Null
}

$SourceDir = Join-Path $PSScriptRoot "skills"
$Skills = Get-ChildItem -Path $SourceDir -Directory

foreach ($Skill in $Skills) {
    $Dest = Join-Path $TargetDir $Skill.Name
    Write-Host "Installing skill: $($Skill.Name)..." -ForegroundColor Yellow
    if (Test-Path $Dest) {
        Remove-Item -Path $Dest -Recurse -Force
    }
    Copy-Item -Path $Skill.FullName -Destination $Dest -Recurse -Force
    Write-Host "  [OK] $($Skill.Name) installed." -ForegroundColor Green
}

Write-Host "`n>>> All skills successfully installed globally! Restart or open Antigravity to discover them." -ForegroundColor Green
