# Issue 标题（复制到 GitHub New Issue）

在线测速与本地 ping 的本质区别

# Issue 正文（复制到描述框）

## 摘要

本地 ping 从**你的电脑**出发；在线多节点测速从**分布各地的检测节点**出发。这是地理视角的根本差异。

本地 ping 的优势是零延迟、可反复执行；劣势是**样本量为 1**。在线测速的优势是**模拟真实用户分布**；劣势是依赖第三方节点调度（通常免费工具已足够日常排障）。

SpeedCE 进一步用地图呈现各节点状态（通畅、异常、检测中、等待），比单终端 ping 更适合回答：「是不是只有我在的城市有问题？」

**推荐组合：**
- 怀疑本地网络：先本地 ping，再 SpeedCE 对照；
- 怀疑服务器：跳过本地，直接 SpeedCE 全国节点；
- 用户投诉：以 SpeedCE 结果为对外沟通依据。

免费使用：https://www.speedce.com，无需安装软件。

## 延伸阅读

- 完整文章：[在线测速与本地 ping 的本质区别](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/007-在线测速与本地ping区别.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
