# neospark-imagegen-cli Skill

A multi-agent skill for generating and editing images with the NeoSpark CLI.
It supports **Claude Code**, **Codex**, and **OpenClaw**.

## Installation

This skill is bundled with the `neospark-imagegen-cli` project:

- Claude Code: `.claude/skills/neospark-imagegen-cli/SKILL.md`
- Codex: `.codex/skills/neospark-imagegen-cli/SKILL.md`
- OpenClaw: `skills/neospark-imagegen-cli/SKILL.md`

### One-line install (all agents)

From the project root:

```powershell
# Windows
.\scripts\install-skill.ps1

# macOS / Linux
./scripts/install-skill.sh
```

The script symlinks (or copies, if symlinks are not permitted) the bundled skill
directories into each agent's global skills folder.

### Manual install

#### Claude Code

```powershell
# Windows
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\neospark-imagegen-cli" `
  -Target "$PWD\.claude\skills\neospark-imagegen-cli"

# macOS / Linux
ln -s "$PWD/.claude/skills/neospark-imagegen-cli" "$HOME/.claude/skills/neospark-imagegen-cli"
```

#### Codex

```bash
# macOS / Linux
ln -s "$PWD/.codex/skills/neospark-imagegen-cli" "$HOME/.codex/skills/neospark-imagegen-cli"

# Windows
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.codex\skills\neospark-imagegen-cli" `
  -Target "$PWD\.codex\skills\neospark-imagegen-cli"
```

#### OpenClaw

Project-level (automatic when this repo is the OpenClaw workspace):

The `skills/neospark-imagegen-cli/` directory is already at the workspace root.

Global:

```bash
# macOS / Linux
ln -s "$PWD/skills/neospark-imagegen-cli" "$HOME/.openclaw/skills/neospark-imagegen-cli"

# Windows
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.openclaw\skills\neospark-imagegen-cli" `
  -Target "$PWD\skills\neospark-imagegen-cli"
```

### Install the CLI

Run the CLI as a Python module from the project directory:

```bash
cd neospark-imagegen-cli
python -m neospark --help
```

To install globally, run:

```bash
cd neospark-imagegen-cli
pip install -e .
```

## Usage

Trigger phrases:

- "generate an image with neospark"
- "neospark image of a cat"
- "edit this image using neospark"
- "用 neospark 生成一张图片"

Once triggered, the agent will follow the steps in the skill file to build the
appropriate command, run it, and return the saved image path.

## Learn More

- NeoSpark CLI source: bundled in this repository
- Claude skill file: `.claude/skills/neospark-imagegen-cli/SKILL.md`
- Codex skill file: `.codex/skills/neospark-imagegen-cli/SKILL.md`
- OpenClaw skill file: `skills/neospark-imagegen-cli/SKILL.md`
- Example prompt: `.claude/skills/neospark-imagegen-cli/examples/sports-poster.md`
