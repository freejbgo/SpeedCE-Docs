# Issue 标题

问：上了 IPv6，怎么确认用户真的能访问？

---

# Issue 正文

## 问题

DNS 已配 A + AAAA，服务器也监听了 IPv6，是否就算 IPv6 可用了？

## 回答

需要**分别测 IPv4 和 IPv6**，不能假设双栈一定都通。

常见坑：

- 只开了 IPv4 防火墙，IPv6 端口未放行
- Nginx 只 `listen 80`，未 `listen [::]:80`
- CDN 只代理了 IPv4

分别用 IPv4 地址和 IPv6 地址做 HTTPS 检测，对比地图是否一致。

---

## 延伸阅读

- [005-IPv4-IPv6双栈测速验证.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/005-IPv4-IPv6双栈测速验证.md)

---

**建议 Labels：** `question, troubleshooting`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
