---
name: neospark-cli
description: Generate and edit images using the NeoSpark CLI from natural language prompts within Claude Code.
triggers:
  - generate image with neospark
  - neospark image
  - create image using neospark
  - edit image with neospark
  - neospark 生成图片
  - 用 neospark 生成
  - neospark 图生图
  - neospark 文生图
author: NeoSpark CLI Team
version: 1.0.0
date: 2026-07-06
---

# NeoSpark CLI Skill

This skill lets you generate, edit, and manage AI images directly from Claude Code using the NeoSpark command-line interface.

## When to Use

Use this skill when the user wants to:

- Generate an image from a text prompt
- Edit an existing image with a new prompt
- Combine multiple reference images into one output
- List, download, or manage generated images and sessions
- Batch-generate images or inspect billing history

## Cross-Platform Support

The underlying NeoSpark CLI is written in Python and supports **Windows, macOS, and Linux**.

| Platform | Installation | Executable name |
|---|---|---|
| Windows | `pip install -e .` or PyInstaller binary | `neospark.exe` |
| macOS | `pip install -e .` or PyInstaller binary | `neospark` |
| Linux | `pip install -e .` or PyInstaller binary | `neospark` |

Claude should locate the CLI using the following priority:

1. `neospark` command in `PATH` (pip install)
2. Project-specific binary: `dist/neospark` or `dist/neospark.exe`
3. Python module: `python -m neospark` from the project directory

## Auto-Installation

Before running any image generation command, check whether `neospark` is available. If not, run the bundled install script:

```bash
python3 .claude/skills/neospark-cli/scripts/install.py
```

The install script will:

1. Check if `neospark` is already in `PATH`
2. If Python is available, install the CLI from the bundled source with `pip install -e .`
3. If Python is unavailable, download the matching pre-built binary from GitHub Releases
4. Verify the installation by running `neospark --version`

If the install script fails, ask the user to either:
- Install Python 3.8+ and re-run the script, or
- Download the correct binary manually from Releases

## How to Use

### Authentication

If `NEOSPARK_API_KEY` is not already set, ask the user for their key and run:

```bash
neospark auth login --api-key <key>
```

Or set the environment variable for the session:

```bash
export NEOSPARK_API_KEY=<key>
```

### Text-to-Image

```bash
neospark generate "<prompt>" \
  --resolution 1K \
  --aspect 16:9 \
  --output ./output.png
```

### Image-to-Image

```bash
neospark generate "<prompt>" \
  --ref ./input.jpg \
  --output ./output.png
```

### Multi-Reference Image

```bash
neospark generate "<prompt>" \
  --ref ./a.jpg --ref ./b.jpg --ref ./c.jpg \
  --output ./output.png
```

### Check Status

```bash
neospark status <message_id>
```

### List Sessions / Images / Billing

```bash
neospark sessions list
neospark images list
neospark billing
```

## Default Behavior

- Default model: `gpt-image-2`
- Default resolution: `1K`
- Default aspect ratio: `1:1`
- Default provider: `tengda` (auto-detected; use `gemini-` prefixed models for Gemini)

## Important Notes

- Image-to-image and multi-reference generation currently work best with `gpt-image-2`.
- The `--zip` batch download option is not reliable due to a server-side issue; download images individually instead.
- All generated files are saved to the current working directory unless `--output-dir` is specified.
- The CLI supports `--json` output for scripting and automation.
- On Windows, paths use backslashes; on macOS/Linux, use forward slashes.

## References

- CLI source: `D:\project\skills_creator\neospark_cli` (Windows) or project root
- Standalone executable: `dist/neospark` (macOS/Linux) or `dist/neospark.exe` (Windows)
- API documentation: `D:\project\skills_creator\ecommerce_detailed_page_expert\IMAGE_GENERATION_API(1).md`
