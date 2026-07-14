# neospark-imagegen-cli Skill

A Claude Code skill for generating and editing images with the NeoSpark CLI.

## What It Does

This skill turns natural-language image requests into `neospark` CLI commands. You can generate images from text, edit images with new prompts, blend multiple reference images, and manage your generation history.

## Installation

This skill is bundled with the `neospark-imagegen-cli` project. When the project is loaded into Claude Code, the skill is automatically available.

Run the CLI as a Python module from the project directory:

```bash
cd D:\project\skills_creator\neospark-imagegen-cli
python -m neospark --help
```

To install globally, first install the package from source:

```bash
cd D:\project\skills_creator\neospark-imagegen-cli
pip install -e .
```

Then symlink the skill directory into your Claude skills folder:

```bash
# Windows (PowerShell, as admin)
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\neospark-imagegen-cli" `
  -Target "D:\project\skills_creator\neospark-imagegen-cli\.claude\skills\neospark-imagegen-cli"

# macOS / Linux
ln -s "D:/project/skills_creator/neospark-imagegen-cli/.claude/skills/neospark-imagegen-cli" \
      "$HOME/.claude/skills/neospark-imagegen-cli"
```

## Usage

Trigger phrases:

- "generate an image with neospark"
- "neospark image of a cat"
- "edit this image using neospark"
- "用 neospark 生成一张图片"

Once triggered, Claude will build the appropriate `python -m neospark generate` command, run it, and return the saved image path.

## Examples

### Generate a poster

```bash
python -m neospark generate "a minimalist sports poster, navy blue and neon green" \
  --resolution 1K --aspect 16:9 --output ./poster.png
```

### Edit a photo

```bash
python -m neospark generate "change the background to a studio gradient" \
  --ref ./photo.jpg --output ./photo-edited.png
```

### Blend references

```bash
python -m neospark generate "combine these styles into a single hero image" \
  --ref ./a.jpg --ref ./b.jpg --output ./combined.png
```

## Configuration

Set your NeoSpark API key before generating:

```bash
python -m neospark auth login --api-key np_xxxxx
```

Or use the environment variable:

```bash
export NEOSPARK_API_KEY=np_xxxxx
```

## Learn More

- NeoSpark CLI source: `D:\project\skills_creator\neospark-imagegen-cli`
- API documentation: `D:\project\skills_creator\neospark-imagegen-cli\IMAGE_GENERATION_API(1).md`
