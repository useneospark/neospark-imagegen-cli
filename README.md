# NeoSpark CLI（Python 版） / NeoSpark CLI (Python)

NeoSpark 图片生成 API 的跨平台命令行封装。支持文生图、图生图、多参考图、会话管理、图片下载、扣费查询等功能。

A cross-platform command-line wrapper for the NeoSpark image generation API. Supports text-to-image, image-to-image, multiple reference images, session management, image download, billing query, and more.

基于 **Python 3.8+** 开发，使用标准库 `argparse` + `requests`，可通过 **PyInstaller** 打包为独立可执行文件，**客户无需安装 Python**。

Built on **Python 3.8+**, using the standard libraries `argparse` and `requests`. It can be packaged as a standalone executable via **PyInstaller**, so **end users do not need to install Python**.

---

## 安装 / Installation

### 方式一：下载独立可执行文件（推荐） / Option 1: Download the standalone executable (recommended)

从 Releases 下载对应平台二进制：

Download the binary for your platform from the Releases page:

- Windows: `neospark.exe`
- macOS: `neospark`
- Linux: `neospark`

放入 PATH 后即可使用：

Place it in your `PATH` and run:

```bash
neospark --version
```

### 方式二：pip 安装（需要 Python 3.8+） / Option 2: Install via pip (requires Python 3.8+)

```bash
pip install neospark-cli
```

### 方式三：源码运行 / Option 3: Run from source

```bash
cd neospark_cli
pip install -e .
python -m neospark --version
```

---

## 认证 / Authentication

支持三种方式，优先级：命令行参数 > 环境变量 > 配置文件。

Three methods are supported, with the following priority: command-line argument > environment variable > config file.

```bash
# 方式一：保存到配置文件 / Option 1: Save to config file
neospark auth login --api-key np_xxxxx

# 方式二：环境变量 / Option 2: Environment variable
export NEOSPARK_API_KEY=np_xxxxx

# 方式三：每次命令传参 / Option 3: Pass per command
neospark models --api-key np_xxxxx
```

---

## 快速开始 / Quick Start

### 查看模型和价格 / List models and prices

```bash
neospark models
```

### 文生图 / Text-to-image

```bash
neospark generate "一只可爱的猫咪，坐在窗台上" \
  --resolution 1K \
  --aspect 1:1 \
  --output ./cat.png
```

> 默认模型为 `gpt-image-2`（tengda）。如需使用 Gemini 模型，显式指定 `--model gemini-3.1-flash-image-preview`。
>
> The default model is `gpt-image-2` (tengda). To use a Gemini model, explicitly specify `--model gemini-3.1-flash-image-preview`.

### 图生图 / Image-to-image

```bash
neospark generate "把背景换成浅灰色" \
  --ref ./product.jpg \
  --output ./result.png
```

### 多参考图 / Multiple reference images

```bash
neospark generate "融合这些图片的风格" \
  --ref ./a.jpg --ref ./b.jpg --ref ./c.jpg \
  --output ./merged.png
```

---

## 命令参考 / Command Reference

### `neospark generate <prompt>`

| 选项 / Option | 默认值 / Default | 说明 / Description |
|---|---|---|
| `--model` | `gpt-image-2` | 模型 ID / Model ID |
| `--resolution` | `1K` | `512`, `1K`, `2K`, `3K`, `4K` |
| `--aspect` | `1:1` | 宽高比 / Aspect ratio |
| `--negative-prompt` | `""` | 负向提示词 / Negative prompt |
| `--num-images` | `1` | 生成数量 1-4 / Number of images to generate (1-4) |
| `--quality` | - | 画质：`low` / `medium` / `high`（仅 gpt-image-2） / Quality: `low` / `medium` / `high` (gpt-image-2 only) |
| `--ref` | - | 本地参考图，可多次使用 / Local reference image; can be used multiple times |
| `--ref-url` | - | 参考图 URL，可多次使用 / Reference image URL; can be used multiple times |
| `--strength` | `0.7` | 参考强度 0.0-1.0 / Reference strength 0.0-1.0 |
| `--output` | | 输出文件路径 / Output file path |
| `--output-dir` | | 输出目录 / Output directory |
| `--zip` | | 以 ZIP 下载 / Download as ZIP |
| `--no-wait` | | 只提交，不轮询 / Submit only, do not poll |
| `--session-id` | | 复用会话 / Reuse session |

### 其他命令 / Other commands

```bash
neospark status <message_id>
neospark images list
neospark images upload ./photo.jpg
neospark images delete up_xxx
neospark sessions list
neospark sessions show ds_xxx
neospark billing
neospark download /uploads/.../cat.png --output ./cat.png
neospark download-zip /uploads/.../a.png /uploads/.../b.png --output ./pack.zip
```

---

## 打包为独立可执行文件 / Packaging as a Standalone Executable

### 安装开发依赖 / Install development dependencies

```bash
pip install -r requirements-dev.txt
```

### 使用 PyInstaller 打包 / Package with PyInstaller

```bash
pyinstaller neospark.spec
```

打包结果：

Build outputs:

- Windows: `dist/neospark.exe`
- macOS/Linux: `dist/neospark`

---

## 跨平台构建（CI） / Cross-Platform Builds (CI)

可通过 GitHub Actions 在 Windows / macOS / Linux 上分别执行 `pyinstaller neospark.spec`，自动发布到 Releases。

You can use GitHub Actions to run `pyinstaller neospark.spec` on Windows, macOS, and Linux, and automatically publish the artifacts to Releases.

---

## Python 版本兼容性 / Python Version Compatibility

- 开发目标 / Development target: Python 3.8+
- 推荐 / Recommended: Python 3.10 / 3.11 / 3.12

---

## 注意事项 / Notes

- 使用 `--ref` 时，CLI 会自动上传本地图片。
- When using `--ref`, the CLI automatically uploads local images.
- `--ref` 和 `--ref-url` 不能同时使用。
- `--ref` and `--ref-url` cannot be used together.
- 所有列表/查询命令支持 `--json` 输出。
- All list/query commands support `--json` output.

---

## License / 许可证

MIT
