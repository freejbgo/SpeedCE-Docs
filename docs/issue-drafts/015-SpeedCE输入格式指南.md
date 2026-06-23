# Issue 标题（复制到 GitHub New Issue）

SpeedCE 支持哪些输入格式？域名与 IP 测速指南

# Issue 正文（复制到描述框）

## 摘要

SpeedCE 输入框兼容多种目标格式，满足不同检测需求：

| 类型 | 示例 |
|------|------|
| 主域名 | example.com |
| www 子域 | www.example.com |
| API 子域 | api.example.com |
| 多级子域 | a.b.example.com |
| IPv4 | 198.51.100.42 |
| IPv6 | 合法 IPv6 格式 |

**注意：** 私有 IP 会被拒绝。输入后选择 HTTP/HTTPS/PING 与节点范围即可。

验 CDN 用域名；验 VPS 裸机可用 IP + PING；验 API 用对应子域 + HTTPS。一个输入框覆盖日常 90% 场景——https://speedce.com/?lang=zh-CN。

## 延伸阅读

- 完整文章：[SpeedCE 支持哪些输入格式？域名与 IP 测速指南](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/015-SpeedCE输入格式指南.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
