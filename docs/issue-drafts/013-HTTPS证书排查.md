# Issue 标题

问：全国 HTTPS 红、HTTP 绿，最先查什么？

---

# Issue 正文

## 问题

用户无法 HTTPS 访问，但 HTTP 可以。开发本地浏览器也没报警。

## 回答

**优先查 SSL 证书：**

1. 是否过期（Let's Encrypt 续签失败很常见）
2. 证书 SAN 是否覆盖所有访问域名
3. 证书链是否完整
4. Nginx `ssl_certificate` 路径是否正确

## 案例

续签脚本静默失败，运维浏览器因缓存未提示，外网多节点 HTTPS 全国红。续签后 5 分钟复测转绿。

建议证书到期前 30 天设提醒，每月 HTTPS 巡检一次。

---

## 延伸阅读

- [018-SpeedCE-HTTPS证书检测.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/018-SpeedCE-HTTPS证书检测.md)
- [024-证书过期地图检测.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/024-证书过期地图检测.md)
- [042-全国HTTPS红HTTP绿.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/042-全国HTTPS红HTTP绿.md)

---

**建议 Labels：** `troubleshooting, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
