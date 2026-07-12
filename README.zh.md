> [English README](README.md) | 中文版

# NeoSpark CLI（Python 版）

NeoSpark 图片生成 API 的跨平台命令行封装。支持文生图、图生图、多参考图、会话管理、图片下载、扣费查询等功能。

基于 **Python 3.8+** 开发，使用标准库 `argparse` + `requests`，可通过 **PyInstaller** 打包为独立可执行文件，**客户无需安装 Python**。

---

## 安装

### 方式一：下载独立可执行文件（推荐）

从 Releases 下载对应平台二进制：

- Windows: `neospark.exe`
- macOS: `neospark`
- Linux: `neospark`

放入 PATH 后即可使用：

```bash
neospark --version
```

### 方式二：pip 安装（需要 Python 3.8+）

```bash
pip install neospark-cli
```

### 方式三：源码运行

```bash
cd neospark_cli
pip install -e .
python -m neospark --version
```

---

## 注册与 API Key

使用 NeoSpark CLI 前，你需要先注册 NeoSpark 账号并获取 API Key。

1. 访问 [NeoSpark](https://useneospark.com/) 并注册 / 登录。
2. 在工作台中，点击左下角头像打开菜单。
   ![打开用户菜单](assets/neospark-menu.png)
3. 选择 **Profile** 进入个人资料页面，然后在 Quick Actions 中点击 **API KEYS**。
   ![API Keys 入口](assets/neospark-profile-apikeys.png)
4. 在 API Keys 页面，点击 **+ CREATE**。
   ![API Keys 列表](assets/neospark-apikeys-list.png)
5. 输入 Key 名称（例如 `neospark-cli`），可选项设置过期时间，然后点击 **CREATE**。
   ![创建 API Key](assets/neospark-create-key-form.png)
6. API Key 只会显示一次，点击 **COPY** 并妥善保存。
   ![复制 API Key](assets/neospark-create-key-result.png)

> API Key 以 `np_` 开头，请妥善保管。如果遗失，只能重新创建。

获取 Key 后，继续阅读下方的 [认证](#认证) 章节。

---

## 认证

支持三种方式，优先级：命令行参数 > 环境变量 > 配置文件。

```bash
# 方式一：保存到配置文件
neospark auth login --api-key np_xxxxx

# 方式二：环境变量
export NEOSPARK_API_KEY=np_xxxxx

# 方式三：每次命令传参
neospark models --api-key np_xxxxx
```

---

## 快速开始

### 查看模型和价格

```bash
neospark models
```

### 文生图

```bash
neospark generate "一只可爱的猫咪，坐在窗台上" \
  --resolution 1K \
  --aspect 1:1 \
  --output ./cat.png
```

> 默认模型为 `gpt-image-2`。如需使用 Gemini 模型，显式指定 `--model gemini-3.1-flash-image-preview`。

### 图生图

```bash
neospark generate "把背景换成浅灰色" \
  --ref ./product.jpg \
  --output ./result.png
```

### 多参考图

```bash
neospark generate "融合这些图片的风格" \
  --ref ./a.jpg --ref ./b.jpg --ref ./c.jpg \
  --output ./merged.png
```

---

## 命令参考

### `neospark generate <prompt>`

| 选项 | 默认值 | 说明 |
|---|---|---|
| `--model` | `gpt-image-2` | 模型 ID |
| `--resolution` | `1K` | `512`, `1K`, `2K`, `3K`, `4K` |
| `--aspect` | `1:1` | 宽高比 |
| `--negative-prompt` | `""` | 负向提示词 |
| `--num-images` | `1` | 生成数量 1-4 |
| `--quality` | - | 画质：`low` / `medium` / `high`（仅 gpt-image-2） |
| `--ref` | - | 本地参考图，可多次使用 |
| `--ref-url` | - | 参考图 URL，可多次使用 |
| `--strength` | `0.7` | 参考强度 0.0-1.0 |
| `--output` | | 输出文件路径 |
| `--output-dir` | | 输出目录 |
| `--zip` | | 以 ZIP 下载 |
| `--no-wait` | | 只提交，不轮询 |
| `--session-id` | | 复用会话 |

### 其他命令

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

## 打包为独立可执行文件

### 安装开发依赖

```bash
pip install -r requirements-dev.txt
```

### 使用 PyInstaller 打包

```bash
pyinstaller neospark.spec
```

打包结果：

- Windows: `dist/neospark.exe`
- macOS/Linux: `dist/neospark`

---

## 跨平台构建（CI）

可通过 GitHub Actions 在 Windows / macOS / Linux 上分别执行 `pyinstaller neospark.spec`，自动发布到 Releases。

---

## Python 版本兼容性

- 开发目标：Python 3.8+
- 推荐：Python 3.10 / 3.11 / 3.12

---

## 注意事项

- 使用 `--ref` 时，CLI 会自动上传本地图片。
- `--ref` 和 `--ref-url` 不能同时使用。
- 所有列表/查询命令支持 `--json` 输出。

---

## License

MIT
