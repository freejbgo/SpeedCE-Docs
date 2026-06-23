# Issue 标题

案例：PING 全超时，但网站其实能开

---

# Issue 正文

## 现象

新手看到 PING 超时就喊宕机，引发误报。

## 原因

很多云主机默认**禁 ICMP**，PING 超时不等于 Web 不可用。

## 正确做法

PING 不通时改测 **HTTPS**。若 HTTPS 全国绿，说明仅 ICMP 被禁。

向非技术用户解释时，两张截图比术语更有效。

---

## 延伸阅读

- [043-PING超时HTTPS正常.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/043-PING超时HTTPS正常.md)
- [019-SpeedCE-PING验VPS.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/019-SpeedCE-PING验VPS.md)

---

**建议 Labels：** `case, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
