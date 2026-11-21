---
name: neospark-imagegen-cli
description: Generate or edit images with the NeoSpark CLI. Use when the user asks for neospark image generation, image-to-image edits, multi-reference blends, or listing generated images.
triggers:
  - neospark image
  - neospark 生成图片
  - neospark 图生图
  - neospark 文生图
---

# neospark-imagegen-cli

Generate, edit, blend, and manage images through the NeoSpark CLI.

Run all commands with `neospark`. If the CLI is not on PATH, run `neospark` from the project root.

## Branches

- **Generate** — text-to-image from a prompt.
- **Edit** — image-to-image with `--ref`.
- **Blend** — multi-reference with multiple `--ref` flags.
- **Batch multi-ref** — one result per reference image via `neospark generate-multi-ref`.
- **E-commerce storyboard** — product nine-grid storyboard via `neospark ecommerce storyboard`.
- **Manage** — list sessions/images or check billing.

## Generate

1. Check authentication: run `neospark auth status`. If not authenticated, ask the user for their API key and run `neospark auth login --api-key <key>`.
2. Build the command: `neospark generate "<prompt>" --output <name> --output-dir <dir>`. `--output` is a base name only — see Constraints.
3. Apply defaults unless the user overrides them: model `gpt-image-2.5-flare`, resolution `1K`, aspect `1:1`. Provider is auto-detected from the model ID (`gemini`, `tengda`, `wavespeed`) and can be overridden with `--provider`.
4. Run the command and capture the output.
5. Read the `[OUT] Image saved: <path>` line from stdout and verify that exact file exists and is non-empty. If no `[OUT]` line appears, run `neospark status <message_id>`.

**Completion criterion**: the output image file exists and is non-empty.

## Edit / Blend

1. Confirm each `--ref` path exists.
2. Build `neospark generate "<prompt>" --ref <path> [--ref <path> ...] --output <name> --output-dir <dir>`.
3. Run and verify the file named on the `[OUT] Image saved:` line exists and is non-empty.

**Completion criterion**: the output image file exists and is non-empty.

## Manage

- List sessions: `neospark sessions list`
- List images: `neospark images list`
- Show billing: `neospark billing`

## Defaults

- Model: `gpt-image-2.5-flare`
- Resolution: `1K`
- Aspect: `1:1`
- Provider: auto-detected from model ID (`gemini`, `tengda`, `wavespeed`)

## Constraints

- Midjourney (`--model midjourney`) supports only `1K` resolution and ignores `--quality`.
- `--quality` is supported by `tengda gpt-image-2`, `gpt-image-2.5`, and `gpt-image-2.6` models.
- `--format` is supported by `gpt-image-2.6` models: `png` (default), `gif`, `webp`.
- Do not use `--zip` for batch downloads; download images individually with `neospark download <image_id>`.
- `--output` is a **base name, not a path** — any directory part is discarded. The location comes from `--output-dir`, which defaults to the current working directory. So `--output ./out/poster.png` writes `<cwd>/poster.png`; use `--output poster --output-dir ./out` instead.
- The extension is inferred from the returned image URL, not from what you type. Pass a bare name (`--output poster`), not `--output poster.png`.
- Several images are returned when the model produces a batch: the names become `<name>_0.ext`, `<name>_1.ext`, … Always take the real path from the `[OUT] Image saved:` lines.
- Image-to-image and multi-reference work best with `gpt-image-2.5-flare`.

## Failure modes

- **Authentication error** — run `neospark auth login --api-key <key>`.
- **Output missing after success message** — run `neospark status <message_id>` and then `neospark download <image_id>` if needed.
- **Midjourney quality/resolution error** — remove `--quality` and ensure resolution is `1K`.

## Examples

- Generate a poster:
  ```bash
  neospark generate "a minimalist sports poster, navy blue and neon green" \
    --resolution 1K --aspect 16:9 --output poster --output-dir ./out
  ```
- Edit a photo:
  ```bash
  neospark generate "change the background to a studio gradient" \
    --ref ./photo.jpg --output photo-edited --output-dir ./out
  ```
- Blend references:
  ```bash
  neospark generate "combine these styles into a single hero image" \
    --ref ./a.jpg --ref ./b.jpg --output combined --output-dir ./out
  ```

For a complex prompt example, see `examples/sports-poster.md`.
