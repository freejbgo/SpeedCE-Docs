# Issue 标题

问：SaaS 很多客户自定义域名，如何批量巡检？

---

# Issue 正文

## 问题

租户用 `client.example.com` CNAME 过来，数量上百如何抽查？

## 回答

- 按套餐分层：VIP 客户全量月度 HTTPS 测速
- 新客户 onboarding 后必测一次
- 平台变更后抽测 10% 租户域名
- 记录异常租户 ID 与地图截图

避免只测平台主域代表全部租户。

---

## 延伸阅读

- [087-SaaS多租户域名巡检.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/087-SaaS多租户域名巡检.md)

---

**建议 Labels：** `question, documentation`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
