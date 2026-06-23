# Issue 标题

问：WordPress 迁机后，除了后台能登录还要测什么？

---

# Issue 正文

## 问题

WP 迁到新主机，后台正常，是否就算迁移成功？

## 回答

还需**全国 HTTPS 可达性**：插件强制 HTTPS、Mixed Content、缓存插件可能导致部分省份异常。

测首页域名中国节点，关注是否仅 HTTPS 异常或某区域超时。不要只在本地刷新验证。

---

## 延伸阅读

- [026-WordPress迁移测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/026-WordPress迁移测速.md)

---

**建议 Labels：** `troubleshooting, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
