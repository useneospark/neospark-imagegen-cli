#!/usr/bin/env bash
# Install the neospark-imagegen-cli skill into Claude Code, Codex, and/or OpenClaw.
#
# Usage:
#   ./scripts/install-skill.sh
#   ./scripts/install-skill.sh claude codex

set -euo pipefail

SKILL_NAME="neospark-imagegen-cli"
PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

declare -A SOURCE_MAP=(
    [claude]="$PROJECT_ROOT/.claude/skills/$SKILL_NAME"
    [codex]="$PROJECT_ROOT/.codex/skills/$SKILL_NAME"
    [openclaw]="$PROJECT_ROOT/skills/$SKILL_NAME"
)

declare -A TARGET_MAP=(
    [claude]="$HOME/.claude/skills/$SKILL_NAME"
    [codex]="$HOME/.codex/skills/$SKILL_NAME"
    [openclaw]="$HOME/.openclaw/skills/$SKILL_NAME"
)

if [[ $# -gt 0 ]]; then
    AGENTS=("$@")
else
    AGENTS=(claude codex openclaw)
fi

for agent in "${AGENTS[@]}"; do
    source="${SOURCE_MAP[$agent]:-}"
    target="${TARGET_MAP[$agent]:-}"

    if [[ -z "$source" ]] || [[ -z "$target" ]]; then
        echo "Unknown agent: $agent" >&2
        continue
    fi

    if [[ ! -d "$source" ]]; then
        echo "Warning: source skill directory not found: $source"
        continue
    fi

    mkdir -p "$(dirname "$target")"
    rm -rf "$target"

    if ln -s "$source" "$target" 2>/dev/null; then
        echo "Installed $agent skill: $target -> $source"
    else
        cp -R "$source" "$target"
        echo "Copied $agent skill (symlink failed): $target"
    fi
done

echo "Done. Restart the agent CLI if it is already running."
