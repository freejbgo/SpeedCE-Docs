# Issue 标题

问：Nginx 反代 / Docker 映射后外网访问失败？

---

# Issue 正文

## 问题

容器内 curl 正常，外网访问 502 或超时。

## 回答

常见原因：

- Docker `-p` 映射错误或未映射 443
- Nginx `proxy_pass` 指错 upstream
- K8s Ingress host/path 规则错误
- 只监听了 127.0.0.1

**内网正常 ≠ 外网可达。** 上线后必须用外网多节点测域名，不能只在容器里自测。

---

## 延伸阅读

- [074-Nginx反代上线拨测.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/074-Nginx反代上线拨测.md)
- [075-Docker端口映射测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/075-Docker端口映射测速.md)
- [076-K8s-Ingress测速.md](https://github.com/freejbgo/SpeedCE-Docs/blob/main/docs/articles/076-K8s-Ingress测速.md)

---

**建议 Labels：** `troubleshooting, question`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
