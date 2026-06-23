# Issue 标题（复制到 GitHub New Issue）

SpeedCE 通畅率怎么解读？统计栏数字完全指南

# Issue 正文（复制到描述框）

## 摘要

SpeedCE 测速完成后，顶部显示：检测节点数、通畅、异常、已跳过、平均延迟。

**通畅** = 成功访问的节点数；**异常** = 超时或失败；**已跳过** = 调度未参与的节点，可忽略。通畅率 = 通畅/(通畅+异常)。若低于 90%，应警惕；低于 70%，基本属故障。

结合地图看异常分布，勿只看平均延迟。https://speedce.com/?lang=zh-CN。

## 延伸阅读

- 完整文章：[SpeedCE 通畅率怎么解读？统计栏数字完全指南](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/061-SpeedCE通畅率解读.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
