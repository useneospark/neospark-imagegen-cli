# Example: Generate a Sports Poster with NeoSpark CLI

## Prompt

> 编辑体育海报，16:9横版——米白色背景；网球运动员的真实摄影，身着白色服装；超紧凑粗体海军蓝双字标题，运动员夹在字母之间；同一标题在后方放大3倍，以极浅灰色呈现；2-3个高度模糊的霓虹黄绿色网球漂浮在画面边缘；主体周围有锐利的手绘霓虹星爆和锯齿涂鸦；右上角橙色"第28期"方框、条形码、栏目标签，以及简短祈使句作为小号正文；配色为海军蓝+霓虹黄绿色+橙色，搭配米白色背景。

## Command

```bash
neospark generate '编辑体育海报，16:9横版——米白色背景；[运动员+动作]的真实摄影，身着白色/近白色服装；超紧凑粗体海军蓝双字标题"[标题]"，运动员夹在字母之间并与字母重叠；同一标题在后方放大约3倍，以极浅灰色呈现，如同失焦的回声；2-3个高度模糊的霓虹黄绿色网球漂浮在画面边缘，作为前景深度层；主体周围有锐利的手绘霓虹星爆和锯齿涂鸦；右上角橙色"第[XX]期"方框、条形码、栏目标签"[标签]"，以及4-6个简短祈使句作为小号正文；配色为海军蓝+霓虹黄绿色+橙色，搭配米白色背景——无统一锐利平面布局，无深色背景，无深色服装，无缺失的前景模糊效果' \
  --resolution 1K \
  --aspect 16:9 \
  --quality medium \
  --output ./sports_poster.png
```

## Result

- Model: `gpt-image-2` (default)
- Resolution: `1K`
- Aspect: `16:9`
- Cost: 7 credits
- Output: `sports_poster.png`

## Notes

- The default model is `gpt-image-2`, which handles complex layout prompts well.
- Use `--quality medium` or `--quality high` for better text and detail rendering.
- Placeholder text like `[标题]` is interpreted by the model; replace with literal text if you need exact wording.
