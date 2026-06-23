# Issue 标题

问：排障时 HTTP、HTTPS、PING 该选哪个？

---

# Issue 正文

## 问题

在线测速有三种协议，随机选一个经常误判。日常巡检到底该用哪个？

## 回答

| 协议 | 测什么 | 何时用 |
|------|--------|--------|
| PING | IP 层连通 | 验 VPS IP、看是否禁 Ping |
| HTTP | 80 端口 Web | 未强制 HTTPS、回源排查 |
| HTTPS | TLS + Web | **日常首选**，最接近用户浏览器 |

推荐顺序：日常 HTTPS 测主域 → 怀疑 IP 层用 PING → 证书问题对比 HTTP/HTTPS 差异。

## 注意

PING 全超时不代表网站挂了，很多云服务器默认禁 ICMP。

---

## 延伸阅读

- [002-HTTP-HTTPS-PING协议详解.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/002-HTTP-HTTPS-PING协议详解.md)

---

**建议 Labels：** `question, documentation`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
