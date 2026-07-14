---
name: neospark-imagegen-cli
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

## How to Use

The skill wraps `neospark` commands. Run it as a Python module from the project directory:

```bash
cd D:\project\skills_creator\neospark-imagegen-cli
python -m neospark <command>
```

If the package is installed (`pip install -e .`), you can also use the `neospark` command directly.

### Authentication

If `NEOSPARK_API_KEY` is not already set, ask the user for their key and run:

```bash
python -m neospark auth login --api-key <key>
```

Or set the environment variable for the session:

```bash
export NEOSPARK_API_KEY=<key>
```

### Text-to-Image

```bash
python -m neospark generate "<prompt>" \
  --resolution 1K \
  --aspect 16:9 \
  --output ./output.png
```

### Image-to-Image

```bash
python -m neospark generate "<prompt>" \
  --ref ./input.jpg \
  --output ./output.png
```

### Multi-Reference Image

```bash
python -m neospark generate "<prompt>" \
  --ref ./a.jpg --ref ./b.jpg --ref ./c.jpg \
  --output ./output.png
```

### Check Status

```bash
python -m neospark status <message_id>
```

### List Sessions / Images / Billing

```bash
python -m neospark sessions list
python -m neospark images list
python -m neospark billing
```

## Default Behavior

- Default model: `gpt-image-2`
- Default resolution: `1K`
- Default aspect ratio: `1:1`
- Default provider: `tengda` (all models currently route through tengda)

## Important Notes

- Image-to-image and multi-reference generation currently work best with `gpt-image-2`.
- Midjourney (`--model midjourney`) supports only `1K` resolution and does not support `--quality`.
- The `--zip` batch download option is not reliable due to a server-side issue; download images individually instead.
- All generated files are saved to the current working directory unless `--output-dir` is specified.
- The CLI supports `--json` output for scripting and automation.

## References

- CLI source: `D:\project\skills_creator\neospark-imagegen-cli`
- API documentation: `D:\project\skills_creator\neospark-imagegen-cli\IMAGE_GENERATION_API(1).md`
