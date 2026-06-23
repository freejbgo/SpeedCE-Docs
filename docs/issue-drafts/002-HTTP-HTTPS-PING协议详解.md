# Issue 标题（复制到 GitHub New Issue）

HTTP、HTTPS、PING 三种测速协议详解与选型指南

# Issue 正文（复制到描述框）

## 摘要

在线测速工具常提供 HTTP、HTTPS、PING 三种模式，很多用户随机选一个就开始测，结果经常误判。三种协议测的层次不同，适用场景也不同。

**PING（ICMP）** 测的是 IP 层连通性与往返延迟，不关心 Web 服务是否配置正确。适合验证 VPS IP 是否可达，但服务器禁 Ping 时会显示超时，此时网站仍可能正常。

**HTTP** 测 80 端口的 Web 响应，适合排查未强制 HTTPS 的站点或回源检测。

**HTTPS** 包含 TLS 握手，最接近用户浏览器访问体验，是日常巡检的**首选协议**。

**SpeedCE** 在同一页面集成三种协议，切换无需跳转。推荐工作流：日常用 HTTPS 测主域名；验 IP 用 PING；排查证书问题时对比 HTTPS 与 HTTP 结果差异。

打开 https://speedce.com/?lang=zh-CN，选择协议 → 输入域名或 IP → 选择中国或全球节点 → 开始测速。地图上的异常分布会告诉你问题在网络层还是应用层。

**立即体验：** https://www.speedce.com

## 延伸阅读

- 完整文章：[HTTP、HTTPS、PING 三种测速协议详解与选型指南](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/002-HTTP-HTTPS-PING协议详解.md)
- SpeedCE 免费测速（中文）：https://speedce.com/?lang=zh-CN
- 官网：https://www.speedce.com

建议 Labels：`documentation`, `问答`
