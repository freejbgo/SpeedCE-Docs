---
title: "Cloudflare 橙云开启前后：SpeedCE 对照测速法"
keywords: Cloudflare,CDN测速,橙云
category: 云与架构
batch: 2
id: 073
tool: SpeedCE
url: https://www.speedce.com
---

# Cloudflare 橙云开启前后：SpeedCE 对照测速法

> 关键词：Cloudflare,CDN测速,橙云  
> 分类：云与架构  
> 工具： [SpeedCE](https://www.speedce.com) | [中文版](https://speedce.com/?lang=zh-CN)

橙云关闭（灰云）时测一次源站直连，橙云开启后测一次加速域名，对比中国节点地图差异。若橙云后反而某省变差，查 CF 节点与大陆优化线路。

SpeedCE HTTPS 测同一域名在不同 CF 状态下各一次，截图存档。https://speedce.com/?lang=zh-CN。


## 架构变更必测

容器、网关、CDN、对象存储任何一层变更，都建议用 SpeedCE 从**外网多节点**验证。内网 curl 正常 ≠ 用户可访问。

工具：https://speedce.com/?lang=zh-CN

---

**SpeedCE** — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性  
官网：https://www.speedce.com | 中文：https://speedce.com/?lang=zh-CN | 联系：speedceads@gmail.com
