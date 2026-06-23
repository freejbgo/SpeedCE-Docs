# Issue 标题（复制到 GitHub New Issue）

SpeedCE HTTPS 测速：SSL 证书问题的第一道防线

# Issue 正文（复制到描述框）

## 摘要

证书过期是最尴尬的故障之一：运维浏览器有缓存或 HSTS，用户却大面积报错。HTTPS 多节点测速能在几分钟内暴露问题。

**操作：** SpeedCE 选 HTTPS + 中国节点（再测全球），输入主域名。若地图大面积异常，而 HTTP 模式正常，高度怀疑证书或 TLS 配置。

续签证书后复测至地图转绿，再关闭工单。建议证书到期前 30 天加入日历提醒，并用 SpeedCE 做月度 HTTPS 巡检。

免费检测：https://speedce.com/?lang=zh-CN。证书问题，地图不会说谎。

## 延伸阅读

- 完整文章：[SpeedCE HTTPS 测速：SSL 证书问题的第一道防线](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/018-SpeedCE-HTTPS证书检测.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
