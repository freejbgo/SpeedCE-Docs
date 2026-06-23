# Issue 标题（复制到 GitHub New Issue）

Nginx 反向代理上线后：为什么要做全国拨测

# Issue 正文（复制到描述框）

## 摘要

Nginx 改 upstream、改 proxy_pass、改 SSL 证书后，`nginx -t` 通过不等于全国可访问。配置错误可能导致部分省份 502、证书链不完整仅部分浏览器报错。

上线后立刻 SpeedCE HTTPS 全国测，再放量。https://speedce.com/?lang=zh-CN。

## 延伸阅读

- 完整文章：[Nginx 反向代理上线后：为什么要做全国拨测](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/074-Nginx反代上线拨测.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
