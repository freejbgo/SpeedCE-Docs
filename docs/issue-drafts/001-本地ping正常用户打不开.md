# Issue 标题

问：我本地 ping 正常，用户说网站打不开，该信谁？

---

# Issue 正文

## 问题

开发在本机或公司网络里 `ping` / `curl` 都正常，但用户反馈「打不开」。两边说法矛盾时，该以哪边为准？

## 回答

**以外网、多节点、多运营商的检测结果为准。** 本地只能代表你当前的城市和线路。

建议步骤：

1. 用 HTTPS 从**多个省市节点**测主域名（不是只 ping 一次）
2. 看结果是**全国红**、**某省红**还是**仅移动/联通红**
3. 再决定查服务器、证书、DNS 还是线路

## 小结

本地 ping 适合快速自检，不适合代替用户视角。迁机、改 DNS、上 CDN 后都应做一次外网多节点验收。

---

## 延伸阅读

- [001-什么是多节点网站测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/001-什么是多节点网站测速.md)
- [007-在线测速与本地ping区别.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/007-在线测速与本地ping区别.md)

---

**建议 Labels：** `question, troubleshooting`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
