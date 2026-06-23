# Issue 标题

问：外网全国红、服务器本地 curl 正常，查什么？

---

# Issue 正文

## 问题

地图全国红，SSH 进去服务正常。

## 回答

优先顺序：云安全组/防火墙 → 443 是否对外 → 证书 → Nginx 是否只 listen 内网 → 上游是否宕机。

地图是「外网视角」，本地 curl 是「本机视角」。先修外网可达，再调 Nginx 性能。

---

## 延伸阅读

- [038-测速异常到Nginx修复.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/038-测速异常到Nginx修复.md)

---

**建议 Labels：** `troubleshooting, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
