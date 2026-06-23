# Issue 标题（复制到 GitHub New Issue）

IPv4 与 IPv6 双栈网站如何用在线工具验证

# Issue 正文（复制到描述框）

## 摘要

IPv6 普及加速，越来越多站点同时支持 IPv4 和 IPv6。双栈配置错误时，可能出现「IPv4 用户正常、IPv6 用户超时」的隐蔽故障，本地测试难以发现。

在线多节点测速工具可分别输入 IPv4 地址与 IPv6 地址，从全国节点验证连通性。SpeedCE 支持 IPv4 / IPv6 输入，配合中国节点与全球节点，可快速判断双栈是否均生效。

**建议步骤：**
1. HTTPS 测域名（走 DNS 解析，含 A/AAAA 记录综合结果）；
2. 若怀疑解析问题，分别测 A 记录 IP 与 AAAA 记录 IP；
3. 对比地图，查看是否存在仅 IPv6 路径异常的区域。

IPv6 故障在部分省份、部分运营商上更常见，多节点视角不可或缺。免费检测：https://www.speedce.com，中文：https://speedce.com/?lang=zh-CN。

2026 年，双栈验证应成为站长标准动作，而非可选项。

## 延伸阅读

- 完整文章：[IPv4 与 IPv6 双栈网站如何用在线工具验证](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/005-IPv4-IPv6双栈测速验证.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
