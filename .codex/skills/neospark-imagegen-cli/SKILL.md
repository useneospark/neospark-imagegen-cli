---
name: neospark-imagegen-cli
description: Generate or edit images with the NeoSpark CLI. Use when the user asks for neospark image generation, image-to-image edits, multi-reference blends, or listing generated images.
---

# neospark-imagegen-cli

Generate, edit, blend, and manage images through the NeoSpark CLI.

Run all commands with `neospark`. If the CLI is not on PATH, run `neospark` from the project root.

## Branches

- **Generate** — text-to-image from a prompt.
- **Edit** — image-to-image with `--ref`.
- **Blend** — multi-reference with multiple `--ref` flags.
- **Manage** — list sessions/images or check billing.

## Generate

1. Check authentication: run `neospark auth status`. If not authenticated, ask the user for their API key and run `neospark auth login --api-key <key>`.
2. Build the command: `neospark generate "<prompt>" --output <path>`.
3. Apply defaults unless the user overrides them: model `gpt-image-2.5-flare`, resolution `1K`, aspect `1:1`, provider `tengda`.
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

- Model: `gpt-image-2.5-flare`
- Resolution: `1K`
- Aspect: `1:1`
- Provider: `tengda` (all models route through tengda)

## Constraints

- Midjourney (`--model midjourney`) supports only `1K` resolution and ignores `--quality`.
- `--quality` is supported by `tengda gpt-image-2` and `gpt-image-2.5` models.
- Do not use `--zip` for batch downloads; download images individually with `neospark download <image_id>`.
- Image-to-image and multi-reference work best with `gpt-image-2.5-flare`.

## Failure modes

- **Authentication error** — run `neospark auth login --api-key <key>`.
- **Output missing after success message** — run `neospark status <message_id>` and then `neospark download <image_id>` if needed.
- **Midjourney quality/resolution error** — remove `--quality` and ensure resolution is `1K`.

## Examples

- Generate a poster:
  ```bash
  neospark generate "a minimalist sports poster, navy blue and neon green" \
    --resolution 1K --aspect 16:9 --output ./poster.png
  ```
- Edit a photo:
  ```bash
  neospark generate "change the background to a studio gradient" \
    --ref ./photo.jpg --output ./photo-edited.png
  ```
- Blend references:
  ```bash
  neospark generate "combine these styles into a single hero image" \
    --ref ./a.jpg --ref ./b.jpg --output ./combined.png
  ```

For a complex prompt example, see `examples/sports-poster.md`.
