# neospark-imagegen-cli Skill

OpenClaw skill for generating and editing images with the NeoSpark CLI.

## Installation

Place this directory (`neospark-imagegen-cli`) in one of the OpenClaw skill search paths:

- Global: `~/.openclaw/skills/neospark-imagegen-cli/`
- Workspace: `./skills/neospark-imagegen-cli/` (inside the OpenClaw workspace)

## Trigger

Use when the user asks for:

- neospark image generation
- neospark 生成图片
- neospark 图生图
- neospark 文生图

## Quick Start

1. Check authentication: `neospark auth status`
2. If needed, log in: `neospark auth login --api-key <key>`
3. Generate: `neospark generate "<prompt>" --output ./image.png`

See `SKILL.md` for the full workflow, defaults, constraints, and failure modes.
