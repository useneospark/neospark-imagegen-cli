#!/usr/bin/env bash
# Install the neospark-imagegen-cli skill for Claude Code, Codex, and OpenClaw.
# Symlinks the bundled skill directories into each agent's global skills folder.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
SKILL_NAME="neospark-imagegen-cli"

install_skill() {
    local name="$1"
    local source_dir="$2"
    local target_dir="$3"

    echo "[$name]"

    if [[ ! -d "$source_dir" ]]; then
        echo "  Source not found: $source_dir. Skipping."
        return
    fi

    mkdir -p "$(dirname "$target_dir")"

    if [[ -L "$target_dir" ]]; then
        rm "$target_dir"
    elif [[ -e "$target_dir" ]]; then
        rm -rf "$target_dir"
    fi

    ln -s "$source_dir" "$target_dir"
    echo "  Linked: $target_dir -> $source_dir"
}

install_skill "Claude Code" \
    "${PROJECT_ROOT}/.claude/skills/${SKILL_NAME}" \
    "${HOME}/.claude/skills/${SKILL_NAME}"

install_skill "Codex" \
    "${PROJECT_ROOT}/.codex/skills/${SKILL_NAME}" \
    "${HOME}/.codex/skills/${SKILL_NAME}"

install_skill "OpenClaw" \
    "${PROJECT_ROOT}/skills/${SKILL_NAME}" \
    "${HOME}/.openclaw/skills/${SKILL_NAME}"

echo ""
echo "Done. Restart your agent or reload skills for changes to take effect."
