<#
.SYNOPSIS
    Install the neospark-imagegen-cli skill into Claude Code, Codex, and/or OpenClaw.

.DESCRIPTION
    Creates symlinks (or copies, if symlinks are not permitted) from the bundled
    skill directories into each agent's global skills folder:

    - Claude Code: ~\.claude\skills\neospark-imagegen-cli
    - Codex:       ~\.codex\skills\neospark-imagegen-cli
    - OpenClaw:    ~\.openclaw\skills\neospark-imagegen-cli

.PARAMETER Agents
    Which agents to install for. Use 'all' (default) to install for every agent.

.EXAMPLE
    .\scripts\install-skill.ps1
    .\scripts\install-skill.ps1 -Agents claude,codex
#>
[CmdletBinding()]
param(
    [ValidateSet("claude", "codex", "openclaw", "all")]
    [string[]]$Agents = @("all")
)

$ErrorActionPreference = "Stop"

$skillName = "neospark-imagegen-cli"
$projectRoot = Split-Path -Parent $PSScriptRoot

$sourceMap = @{
    claude   = Join-Path $projectRoot ".claude\skills\$skillName"
    codex    = Join-Path $projectRoot ".codex\skills\$skillName"
    openclaw = Join-Path $projectRoot "skills\$skillName"
}

$targetMap = @{
    claude   = Join-Path $env:USERPROFILE ".claude\skills\$skillName"
    codex    = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
    openclaw = Join-Path $env:USERPROFILE ".openclaw\skills\$skillName"
}

$selected = if ($Agents -contains "all") { @("claude", "codex", "openclaw") } else { $Agents }

foreach ($agent in $selected) {
    $source = $sourceMap[$agent]
    $target = $targetMap[$agent]

    if (-not (Test-Path $source)) {
        Write-Warning "Source skill directory not found: $source"
        continue
    }

    $targetDir = Split-Path -Parent $target
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Force -Path $targetDir | Out-Null
    }

    if (Test-Path $target) {
        Remove-Item -Recurse -Force $target
    }

    try {
        New-Item -ItemType SymbolicLink -Path $target -Target $source | Out-Null
        Write-Host "Installed $agent skill: $target -> $source" -ForegroundColor Green
    }
    catch {
        Copy-Item -Recurse -Force -Path $source -Destination $target
        Write-Host "Copied $agent skill (symlink requires admin/dev mode): $target" -ForegroundColor Yellow
    }
}

Write-Host "Done. Restart the agent CLI if it is already running." -ForegroundColor Cyan
