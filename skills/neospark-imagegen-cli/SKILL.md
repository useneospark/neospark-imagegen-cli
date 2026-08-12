---
name: neospark-imagegen-cli
description: 使用 NeoSpark CLI 生成或编辑图片。当用户请求 neospark 文生图、图生图、多参考图融合或查看生成记录时触发。
---

# neospark-imagegen-cli

使用 NeoSpark CLI 生成、编辑、融合和管理图片。

## 触发场景

- 用户使用 `neospark` 生成图片
- 文生图、图生图、多参考图融合
- 列出会话 / 图片或查询账单

## 安装 CLI

在运行图片命令前，先确认 `neospark` 可用：

```bash
neospark --version
```

如果命令不存在，从源码安装：

```bash
cd neospark-imagegen-cli
pip install -e .
```

或在项目根目录使用 `python -m neospark` 代替 `neospark`。

## 分支

- **Generate** — 文生图。
- **Edit** — 图生图，使用 `--ref`。
- **Blend** — 多参考图融合，使用多个 `--ref`。
- **Manage** — 列出会话 / 图片或查询账单。

## 文生图

1. 检查登录状态：`neospark auth status`。未登录则请求 API key 并执行 `neospark auth login --api-key <key>`。
2. 构建命令：`neospark generate "<prompt>" --output <path>`。
3. 除非用户覆盖，否则使用默认值：模型 `gpt-image-2`、分辨率 `1K`、比例 `1:1`、提供商 `tengda`。
4. 运行命令并捕获输出。
5. 验证输出文件存在。若不存在，执行 `neospark status <message_id>`。

**完成标准**：输出图片文件存在且非空。

## 图生图 / 多参考融合

1. 确认每个 `--ref` 路径存在。
2. 构建命令：
   `neospark generate "<prompt>" --ref <path> [--ref <path> ...] --output <path>`
3. 运行并验证输出文件存在。

**完成标准**：输出图片文件存在且非空。

## 管理命令

- 列出会话：`neospark sessions list`
- 列出图片：`neospark images list`
- 查询账单：`neospark billing`

## 默认值

- 模型：`gpt-image-2`
- 分辨率：`1K`
- 比例：`1:1`
- 提供商：`tengda`（所有模型均通过 tengda 路由）
- 画质：`low`（仅 `gpt-image-2` 支持 `--quality`）

## 约束

- Midjourney（`--model midjourney`）仅支持 `1K` 分辨率，忽略 `--quality`。
- `--quality` 仅 `tengda gpt-image-2` 支持。
- 批量下载不要使用 `--zip`；使用 `neospark download <image_id>` 逐张下载。
- 图生图和多参考图使用 `gpt-image-2` 效果最佳。

## 失败处理

- **认证错误** — 执行 `neospark auth login --api-key <key>`。
- **成功但无输出文件** — 执行 `neospark status <message_id>`，必要时再执行 `neospark download <image_id>`。
- **Midjourney 画质 / 分辨率错误** — 移除 `--quality` 并确认分辨率为 `1K`。
- **命令未找到** — 在项目根目录使用 `python -m neospark`。

## 示例

生成海报：

```bash
neospark generate "a minimalist sports poster, navy blue and neon green" \
  --resolution 1K --aspect 16:9 --output ./poster.png
```

编辑照片：

```bash
neospark generate "change the background to a studio gradient" \
  --ref ./photo.jpg --output ./photo-edited.png
```

融合参考图：

```bash
neospark generate "combine these styles into a single hero image" \
  --ref ./a.jpg --ref ./b.jpg --output ./combined.png
```
