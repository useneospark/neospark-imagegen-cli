# neospark-cli Skill

A Claude Code skill for generating and editing images with the NeoSpark CLI.

## What It Does

This skill turns natural-language image requests into `neospark` CLI commands. You can generate images from text, edit images with new prompts, blend multiple reference images, and manage your generation history.

## Cross-Platform Installation

The NeoSpark CLI is a Python project that runs on **Windows, macOS, and Linux**.

### Option 1: pip install from source (recommended for development)

```bash
cd neospark_cli
pip install -e .
```

After installation, the `neospark` command is available globally.

### Option 2: standalone executable

Download the pre-built binary for your platform from the Releases page:

| Platform | File | Size |
|---|---|---|
| Windows | `neospark.exe` | ~14 MB |
| macOS | `neospark` | ~14 MB |
| Linux | `neospark` | ~14 MB |

Place it in a directory on your `PATH`, or use the full path in commands.

### Option 3: install as a Claude skill

#### Repository-local (project-specific)

This skill is bundled with the `neospark_cli` project under `.claude/skills/neospark-cli`. When the project is loaded into Claude Code, the skill is automatically available.

#### Global installation

Create a symlink in your Claude skills folder:

```bash
# macOS / Linux
ln -s "/path/to/neospark_cli/.claude/skills/neospark-cli" \
      "$HOME/.claude/skills/neospark-cli"

# Windows PowerShell (as admin)
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\neospark-cli" `
  -Target "D:\project\skills_creator\neospark_cli\.claude\skills\neospark-cli"
```

### Option 4: automatic installation via the skill

If the skill is loaded but the `neospark` command is missing, run the bundled installer:

```bash
python3 .claude/skills/neospark-cli/scripts/install.py
```

The installer detects the OS, checks for Python, and either installs from source or downloads a pre-built binary.

## Usage

Trigger phrases:

- "generate an image with neospark"
- "neospark image of a cat"
- "edit this image using neospark"
- "用 neospark 生成一张图片"
- "neospark 图生图"

Once triggered, Claude will build the appropriate `neospark generate` command, run it, and return the saved image path.

## Examples

### Generate a poster

```bash
neospark generate "a minimalist sports poster, navy blue and neon green" \
  --resolution 1K --aspect 16:9 --output ./poster.png
```

### Edit a photo

```bash
neospark generate "change the background to a studio gradient" \
  --ref ./photo.jpg --output ./photo-edited.png
```

### Blend references

```bash
neospark generate "combine these styles into a single hero image" \
  --ref ./a.jpg --ref ./b.jpg --output ./combined.png
```

## Configuration

Set your NeoSpark API key before generating:

```bash
neospark auth login --api-key np_xxxxx
```

Or use the environment variable:

```bash
export NEOSPARK_API_KEY=np_xxxxx
```

## Learn More

- NeoSpark CLI source: project root
- API documentation: `ecommerce_detailed_page_expert/IMAGE_GENERATION_API(1).md`
