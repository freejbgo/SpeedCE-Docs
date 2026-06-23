# Issue 标题

问：OSS / Vercel / GitHub Pages 国内访问怎么验收？

---

# Issue 正文

## 问题

静态站托管在境外或对象存储，国内用户反馈慢。

## 回答

HTTPS 测绑定域名 + **中国节点地图**：

- 偏远省份高延迟 → 考虑国内 CDN 或备案回源
- 个别省超时 → 查 CNAME、桶策略、防盗链

Vercel 免费版在国内无保证，地图结果可量化「慢在哪」。

---

## 延伸阅读

- [077-OSS静态托管测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/077-OSS静态托管测速.md)
- [078-Vercel国内访问测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/078-Vercel国内访问测速.md)

---

**建议 Labels：** `troubleshooting, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
