# One-Click Installer for Antigravity Custom Skills & MCP Tools (Windows PowerShell)
$ErrorActionPreference = "Stop"

$GeminiConfigDir = Join-Path $HOME ".gemini\config"
$SkillsTargetDir = Join-Path $GeminiConfigDir "skills"
$McpConfigFile   = Join-Path $GeminiConfigDir "mcp_config.json"

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   Antigravity Skills & MCP Automatic Setup" -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Cyan

# 1. Install Skills
Write-Host "`n>>> [1/2] Installing Skills to: $SkillsTargetDir" -ForegroundColor Yellow
if (-not (Test-Path $SkillsTargetDir)) {
    New-Item -ItemType Directory -Path $SkillsTargetDir -Force | Out-Null
}

$SourceDir = Join-Path $PSScriptRoot "skills"
$Skills = Get-ChildItem -Path $SourceDir -Directory

foreach ($Skill in $Skills) {
    $Dest = Join-Path $SkillsTargetDir $Skill.Name
    Write-Host "  -> Installing $($Skill.Name)..." -ForegroundColor White
    if (Test-Path $Dest) {
        Remove-Item -Path $Dest -Recurse -Force
    }
    Copy-Item -Path $Skill.FullName -Destination $Dest -Recurse -Force
    Write-Host "     [OK] $($Skill.Name) installed." -ForegroundColor Green
}

# 2. Configure MCP Servers (Playwright & Chrome DevTools for Browser Automation)
Write-Host "`n>>> [2/2] Configuring MCP Servers in: $McpConfigFile" -ForegroundColor Yellow

$BrowserMcpConfig = @{
    "playwright" = @{
        "command" = "npx"
        "args" = @("-y", "@playwright/mcp@latest")
    }
    "chrome-devtools" = @{
        "command" = "npx"
        "args" = @("-y", "chrome-devtools-mcp@latest")
    }
}

if (-not (Test-Path $McpConfigFile)) {
    $NewConfig = @{ "mcpServers" = $BrowserMcpConfig }
    $NewConfig | ConvertTo-Json -Depth 10 | Set-Content -Path $McpConfigFile -Encoding UTF8
    Write-Host "  -> Created new mcp_config.json with Playwright & Chrome-DevTools!" -ForegroundColor Green
} else {
    try {
        $ExistingContent = Get-Content -Path $McpConfigFile -Raw -Encoding UTF8 | ConvertFrom-Json
        if (-not $ExistingContent.mcpServers) {
            $ExistingContent | Add-Member -MemberType NoteProperty -Name "mcpServers" -Value (New-Object PSObject)
        }

        $AddedCount = 0
        foreach ($server in $BrowserMcpConfig.Keys) {
            if (-not $ExistingContent.mcpServers.$server) {
                $serverObj = [PSCustomObject]$BrowserMcpConfig[$server]
                $ExistingContent.mcpServers | Add-Member -MemberType NoteProperty -Name $server -Value $serverObj
                Write-Host "  -> Added MCP server: $server" -ForegroundColor Green
                $AddedCount++
            } else {
                Write-Host "  -> MCP server '$server' is already configured." -ForegroundColor Gray
            }
        }

        if ($AddedCount -gt 0) {
            $ExistingContent | ConvertTo-Json -Depth 10 | Set-Content -Path $McpConfigFile -Encoding UTF8
            Write-Host "  -> Updated mcp_config.json successfully." -ForegroundColor Green
        }
    } catch {
        Write-Host "  [!] Could not automatically merge mcp_config.json. Please refer to mcp_config.example.json." -ForegroundColor DarkYellow
    }
}

Write-Host "`n==========================================================" -ForegroundColor Green
Write-Host " [SUCCESS] Setup complete!" -ForegroundColor Green
Write-Host " Skills installed: $(($Skills | ForEach-Object { $_.Name }) -join ', ')" -ForegroundColor White
Write-Host " Restart Antigravity to activate the newly added tools." -ForegroundColor Cyan
Write-Host "==========================================================" -ForegroundColor Green
