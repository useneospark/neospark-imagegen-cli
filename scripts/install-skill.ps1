#Requires -Version 5.1
<#
.SYNOPSIS
    Install the neospark-imagegen-cli skill for Claude Code, Codex, and OpenClaw.
.DESCRIPTION
    Symlinks (or copies, if symlinks are not permitted) the bundled skill
    directories into each agent's global skills folder.
#>
[CmdletBinding()]
param()

$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $PSScriptRoot
$skillName = "neospark-imagegen-cli"

$agents = @(
    @{
        Name = "Claude Code"
        Source = Join-Path $projectRoot ".claude\skills\$skillName"
        Target = Join-Path $env:USERPROFILE ".claude\skills\$skillName"
    },
    @{
        Name = "Codex"
        Source = Join-Path $projectRoot ".codex\skills\$skillName"
        Target = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
    },
    @{
        Name = "OpenClaw"
        Source = Join-Path $projectRoot "skills\$skillName"
        Target = Join-Path $env:USERPROFILE ".openclaw\skills\$skillName"
    }
)

function Install-AgentSkill {
    param([hashtable]$Agent)

    Write-Host "[$($Agent.Name)]" -ForegroundColor Cyan

    if (-not (Test-Path $Agent.Source)) {
        Write-Warning "Source not found: $($Agent.Source). Skipping."
        return
    }

    $targetDir = Split-Path -Parent $Agent.Target
    if (-not (Test-Path $targetDir)) {
        New-Item -ItemType Directory -Path $targetDir -Force | Out-Null
    }

    if (Test-Path $Agent.Target) {
        $existing = Get-Item $Agent.Target
        if ($existing.Attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            Write-Host "  Removing existing symlink..."
            Remove-Item $Agent.Target -Force
        } else {
            Write-Host "  Removing existing copy..."
            Remove-Item $Agent.Target -Recurse -Force
        }
    }

    try {
        New-Item -ItemType SymbolicLink -Path $Agent.Target -Target $Agent.Source -Force | Out-Null
        Write-Host "  Linked: $($Agent.Target) -> $($Agent.Source)" -ForegroundColor Green
    } catch {
        Write-Host "  Symlink failed, copying instead..."
        Copy-Item -Path $Agent.Source -Destination $Agent.Target -Recurse -Force
        Write-Host "  Copied: $($Agent.Target)" -ForegroundColor Green
    }
}

foreach ($agent in $agents) {
    Install-AgentSkill -Agent $agent
}

Write-Host "`nDone. Restart your agent or reload skills for changes to take effect." -ForegroundColor Green
