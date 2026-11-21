#!/usr/bin/env python3
"""Build a directly installable zip for the neospark-imagegen-cli agent skill.

The package layout is:

    neospark-imagegen-cli-skill-<version>/
        README.md
        install.ps1
        install.sh
        agents/claude/neospark-imagegen-cli/...
        agents/codex/neospark-imagegen-cli/...
        agents/openclaw/neospark-imagegen-cli/...

The canonical skill content comes from .claude/skills/neospark-imagegen-cli.
Agent variants only differ in SKILL.md front matter.

Usage:
    python scripts/build-skill-zip.py [--version 0.1.0] [--output path.zip]
"""
from __future__ import annotations

import argparse
import re
import shutil
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "neospark-imagegen-cli"
SOURCE_SKILL = REPO_ROOT / ".claude" / "skills" / SKILL_NAME
DEFAULT_VERSION = "0.1.0"
IGNORE = shutil.ignore_patterns("__pycache__", "*.pyc", "*.pyo")

TRIGGERS_BLOCK = re.compile(r"^triggers:\n(?:[ \t]+.*\n)+", re.MULTILINE)
FRONTMATTER = re.compile(r"\A---\r?\n.*?\r?\n---\r?\n\r?\n", re.DOTALL)


PACKAGE_README = """# neospark-imagegen-cli — Agent Skill

可直接安装的 Agent Skill 包，支持 **Claude Code**、**Codex** 和 **OpenClaw**。

A ready-to-install skill package for Claude Code, Codex, and OpenClaw.

---

## 快速安装 / Quick install

### Windows 10 / 11

解压后进入本目录，运行：

```powershell
# 安装到全部 Agent（默认）
powershell -ExecutionPolicy Bypass -File .\\install.ps1

# 只安装到 Claude Code
powershell -ExecutionPolicy Bypass -File .\\install.ps1 -Agent claude

# 卸载
powershell -ExecutionPolicy Bypass -File .\\install.ps1 -Uninstall
```

### macOS / Linux

```bash
chmod +x install.sh
./install.sh                    # 全部 Agent
./install.sh --agent claude     # 只安装 Claude Code
./install.sh --uninstall        # 卸载
```

安装后重启 Agent，或重新加载 skills 使改动生效。

## 手动安装 / Manual install

把对应的技能目录复制到 Agent 的全局 skills 目录：

| Agent | 源目录 / Source | 目标目录 / Target |
| --- | --- | --- |
| Claude Code | `agents/claude/neospark-imagegen-cli/` | `~/.claude/skills/neospark-imagegen-cli/` |
| Codex | `agents/codex/neospark-imagegen-cli/` | `~/.codex/skills/neospark-imagegen-cli/` |
| OpenClaw | `agents/openclaw/neospark-imagegen-cli/` | `~/.openclaw/skills/neospark-imagegen-cli/` |

Windows 下 `~` 即 `%USERPROFILE%`。

## 前置条件 / Prerequisite

技能通过 `neospark` CLI 调用 NeoSpark 图片 API，需要先安装 CLI：

```bash
pip install neospark-cli
# 或从 https://github.com/useneospark/neospark-imagegen-cli/releases 下载可执行文件
```

安装后配置 API Key：

```bash
neospark auth login --api-key <your-api-key>
```

验证：

```bash
neospark --version
neospark auth status
```

## 使用 / Usage

安装后直接用自然语言触发，例如：

- "用 neospark 生成一张猫咪在窗台上的图片"
- "neospark 图生图，把背景换成影棚渐变"
- "neospark image of a minimalist sports poster"

技能会按 `SKILL.md` 中的流程构建命令、执行并返回图片路径。

更多细节见 `agents/<agent>/neospark-imagegen-cli/SKILL.md`。
"""


INSTALL_PS1 = r"""#Requires -Version 5.1
<#
.SYNOPSIS
    Install or uninstall the neospark-imagegen-cli skill.
.DESCRIPTION
    Copies the bundled skill into the global skills directory of the selected
    agent (Claude Code, Codex, or OpenClaw).
.PARAMETER Agent
    Which agent to install for: all (default), claude, codex, or openclaw.
.PARAMETER Uninstall
    Remove the skill from the selected agent(s) instead of installing.
.EXAMPLE
    .\install.ps1
    .\install.ps1 -Agent claude
    .\install.ps1 -Uninstall
#>
[CmdletBinding()]
param(
    [ValidateSet("all", "claude", "codex", "openclaw")]
    [string]$Agent = "all",

    [switch]$Uninstall
)

$ErrorActionPreference = "Stop"

$packageRoot = $PSScriptRoot
$skillName = "neospark-imagegen-cli"

$agents = @{
    claude = @{
        Label  = "Claude Code"
        Source = Join-Path $packageRoot "agents\claude\$skillName"
        Target = Join-Path $env:USERPROFILE ".claude\skills\$skillName"
    }
    codex = @{
        Label  = "Codex"
        Source = Join-Path $packageRoot "agents\codex\$skillName"
        Target = Join-Path $env:USERPROFILE ".codex\skills\$skillName"
    }
    openclaw = @{
        Label  = "OpenClaw"
        Source = Join-Path $packageRoot "agents\openclaw\$skillName"
        Target = Join-Path $env:USERPROFILE ".openclaw\skills\$skillName"
    }
}

$selected = if ($Agent -eq "all") {
    @("claude", "codex", "openclaw")
} else {
    @($Agent)
}

foreach ($key in $selected) {
    $current = $agents[$key]
    Write-Host "[$($current.Label)]" -ForegroundColor Cyan

    if ($Uninstall) {
        if (Test-Path $current.Target) {
            Remove-Item -Path $current.Target -Recurse -Force
            Write-Host "  Removed: $($current.Target)" -ForegroundColor Green
        } else {
            Write-Host "  Not installed."
        }
        continue
    }

    if (-not (Test-Path $current.Source)) {
        Write-Warning "  Source not found: $($current.Source). Skipping."
        continue
    }

    $targetParent = Split-Path -Parent $current.Target
    if (-not (Test-Path $targetParent)) {
        New-Item -ItemType Directory -Path $targetParent -Force | Out-Null
    }

    if (Test-Path $current.Target) {
        Remove-Item -Path $current.Target -Recurse -Force
    }

    Copy-Item -Path $current.Source -Destination $current.Target -Recurse -Force
    Write-Host "  Installed: $($current.Target)" -ForegroundColor Green
}

if ($Uninstall) {
    Write-Host "`nDone. Restart your agent for the removal to take effect." -ForegroundColor Green
} else {
    Write-Host "`nDone. Restart your agent or reload skills for changes to take effect." -ForegroundColor Green
}
"""


INSTALL_SH = r"""#!/usr/bin/env bash
# Install or uninstall the neospark-imagegen-cli skill for
# Claude Code, Codex, and OpenClaw.

set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_NAME="neospark-imagegen-cli"
AGENT="all"
UNINSTALL=0

usage() {
    cat <<'EOF'
Usage: ./install.sh [options]

Options:
  --agent, -a <name>   Target agent: all (default) | claude | codex | openclaw
  --uninstall, -u      Remove the skill from the selected agent(s)
  --help, -h           Show this help message
EOF
}

while [[ $# -gt 0 ]]; do
    case "$1" in
        --agent|-a)
            if [[ $# -lt 2 ]]; then
                echo "Error: $1 requires a value." >&2
                usage >&2
                exit 1
            fi
            AGENT="$2"
            shift 2
            ;;
        --agent=*)
            AGENT="${1#*=}"
            shift
            ;;
        --uninstall|-u)
            UNINSTALL=1
            shift
            ;;
        --help|-h)
            usage
            exit 0
            ;;
        *)
            echo "Unknown option: $1" >&2
            usage >&2
            exit 1
            ;;
    esac
done

case "$AGENT" in
    all) AGENTS=(claude codex openclaw) ;;
    claude|codex|openclaw) AGENTS=("$AGENT") ;;
    *)
        echo "Unknown agent: $AGENT (choose: all, claude, codex, openclaw)" >&2
        exit 1
        ;;
esac

for key in "${AGENTS[@]}"; do
    case "$key" in
        claude)
            label="Claude Code"
            target="$HOME/.claude/skills/$SKILL_NAME"
            ;;
        codex)
            label="Codex"
            target="$HOME/.codex/skills/$SKILL_NAME"
            ;;
        openclaw)
            label="OpenClaw"
            target="$HOME/.openclaw/skills/$SKILL_NAME"
            ;;
    esac

    source_dir="$PACKAGE_ROOT/agents/$key/$SKILL_NAME"

    echo "[$label]"

    if [[ $UNINSTALL -eq 1 ]]; then
        if [[ -e "$target" || -L "$target" ]]; then
            rm -rf "$target"
            echo "  Removed: $target"
        else
            echo "  Not installed."
        fi
        continue
    fi

    if [[ ! -d "$source_dir" ]]; then
        echo "  Source not found: $source_dir. Skipping."
        continue
    fi

    mkdir -p "$(dirname "$target")"
    if [[ -e "$target" || -L "$target" ]]; then
        rm -rf "$target"
    fi

    cp -R "$source_dir" "$target"
    echo "  Installed: $target"
done

if [[ $UNINSTALL -eq 1 ]]; then
    echo ""
    echo "Done. Restart your agent for the removal to take effect."
else
    echo ""
    echo "Done. Restart your agent or reload skills for changes to take effect."
fi
"""


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as handle:
        handle.write(text)


def build_variant(package_dir: Path, variant: str) -> Path:
    """Copy the canonical skill and adjust SKILL.md front matter per agent."""
    target = package_dir / "agents" / variant / SKILL_NAME
    shutil.copytree(SOURCE_SKILL, target, ignore=IGNORE)

    skill_md = target / "SKILL.md"
    text = skill_md.read_text(encoding="utf-8")

    if variant == "codex":
        text = TRIGGERS_BLOCK.sub("", text, count=1)
    elif variant == "openclaw":
        text = FRONTMATTER.sub("", text, count=1)

    write_text(skill_md, text)
    return target


def create_zip(package_dir: Path, output_zip: Path) -> None:
    output_zip.parent.mkdir(parents=True, exist_ok=True)
    if output_zip.exists():
        output_zip.unlink()

    files = sorted(path for path in package_dir.rglob("*") if path.is_file())
    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as archive:
        for path in files:
            archive.write(path, path.relative_to(package_dir.parent).as_posix())

    print(f"Wrote {output_zip} ({len(files)} files, {output_zip.stat().st_size} bytes)")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--version", default=DEFAULT_VERSION,
                        help=f"package version (default: {DEFAULT_VERSION})")
    parser.add_argument("--output", type=Path, default=None,
                        help="output zip path")
    args = parser.parse_args()

    if not (SOURCE_SKILL / "SKILL.md").is_file():
        print(f"Skill source not found: {SOURCE_SKILL}", file=sys.stderr)
        return 1

    package_name = f"{SKILL_NAME}-skill-{args.version}"
    package_dir = REPO_ROOT / "build" / "skill-zip" / package_name
    if package_dir.exists():
        shutil.rmtree(package_dir)
    package_dir.mkdir(parents=True)

    write_text(package_dir / "README.md", PACKAGE_README)
    write_text(package_dir / "install.ps1", INSTALL_PS1)
    write_text(package_dir / "install.sh", INSTALL_SH)
    (package_dir / "install.sh").chmod(0o755)

    for variant in ("claude", "codex", "openclaw"):
        build_variant(package_dir, variant)
        print(f"Bundled variant: {variant}")

    output_zip = args.output or (REPO_ROOT / f"{package_name}.zip")
    create_zip(package_dir, output_zip)
    return 0


if __name__ == "__main__":
    sys.exit(main())
