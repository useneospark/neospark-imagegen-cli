---
name: neospark-imagegen-cli
description: Generate or edit images with the NeoSpark CLI. Use when the user asks for neospark image generation, image-to-image edits, multi-reference blends, or listing generated images.
---

# neospark-imagegen-cli

Generate, edit, blend, and manage images through the NeoSpark CLI.

Use this skill when the user asks for NeoSpark image generation, image-to-image edits, multi-reference blends, or listing generated images.

## Installation

This skill is bundled with the `neospark-imagegen-cli` project under `.codex/skills/neospark-imagegen-cli/`.

To make it available everywhere in Codex CLI, symlink or copy it into the global Codex skills directory:

```bash
# Linux / macOS
ln -s "$PWD/.codex/skills/neospark-imagegen-cli" "$HOME/.codex/skills/neospark-imagegen-cli"

# Windows PowerShell (admin)
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.codex\skills\neospark-imagegen-cli" `
  -Target "$PWD\.codex\skills\neospark-imagegen-cli"
```

The NeoSpark CLI itself must also be installed. If `neospark --version` fails, install the package:

```bash
cd neospark-imagegen-cli
pip install -e .
```

## CLI availability

Before running image commands, verify `neospark` is on PATH:

```bash
neospark --version
```

If the command is not found and you are inside the project directory, use `python -m neospark` instead of `neospark`.

## Branches

- **Generate** — text-to-image from a prompt.
- **Edit** — image-to-image with `--ref`.
- **Blend** — multi-reference with multiple `--ref` flags.
- **Manage** — list sessions/images or check billing.

## Generate

1. Check authentication: `neospark auth status`. If not authenticated, ask the user for their API key and run `neospark auth login --api-key <key>`.
2. Build the command: `neospark generate "<prompt>" --output <path>`.
3. Apply defaults unless the user overrides them: model `gpt-image-2`, resolution `1K`, aspect `1:1`, provider `tengda`.
4. Run the command and capture the output.
5. Verify the output file exists. If not, run `neospark status <message_id>`.

**Completion criterion**: the output image file exists and is non-empty.

## Edit / Blend

1. Confirm each `--ref` path exists.
2. Build `neospark generate "<prompt>" --ref <path> [--ref <path> ...] --output <path>`.
3. Run and verify the output file exists.

**Completion criterion**: the output image file exists and is non-empty.

## Manage

- List sessions: `neospark sessions list`
- List images: `neospark images list`
- Show billing: `neospark billing`

## Defaults

- Model: `gpt-image-2`
- Resolution: `1K`
- Aspect: `1:1`
- Provider: `tengda` (all models route through tengda)
- Quality: `low` (default; only `gpt-image-2` supports `--quality`)

## Constraints

- Midjourney (`--model midjourney`) supports only `1K` resolution and ignores `--quality`.
- `--quality` is supported only by `tengda gpt-image-2`.
- Do not use `--zip` for batch downloads; download images individually with `neospark download <image_id>`.
- Image-to-image and multi-reference work best with `gpt-image-2`.

## Failure modes

- **Authentication error** — run `neospark auth login --api-key <key>`.
- **Output missing after success message** — run `neospark status <message_id>` and then `neospark download <image_id>` if needed.
- **Midjourney quality/resolution error** — remove `--quality` and ensure resolution is `1K`.
- **Command not found** — install the CLI with `pip install -e .` from the project root, or use `python -m neospark` when inside the project root.

## Examples

Generate a poster:

```bash
neospark generate "a minimalist sports poster, navy blue and neon green" \
  --resolution 1K --aspect 16:9 --output ./poster.png
```

Edit a photo:

```bash
neospark generate "change the background to a studio gradient" \
  --ref ./photo.jpg --output ./photo-edited.png
```

Blend references:

```bash
neospark generate "combine these styles into a single hero image" \
  --ref ./a.jpg --ref ./b.jpg --output ./combined.png
```
