---
title: "阿里云 ECS 迁机后 SpeedCE 验收三步法"
keywords: 阿里云ECS,迁机验收,服务器迁移
category: 云与架构
batch: 2
id: 071
tool: SpeedCE
url: https://www.speedce.com
---

# 阿里云 ECS 迁机后 SpeedCE 验收三步法

> 关键词：阿里云ECS,迁机验收,服务器迁移  
> 分类：云与架构  
> 工具： [SpeedCE](https://www.speedce.com) | [中文版](https://speedce.com/?lang=zh-CN)

ECS 换实例、换地域、换 IP 后：① HTTPS + 中国节点测域名；② 三网各筛选一次；③ 全球节点测海外用户（如有）。

安全组放行 80/443 后仍全国红，查 Nginx 与证书。阿里云控制台「本地正常」不能代替全国测速。工具：https://speedce.com/?lang=zh-CN。


## 架构变更必测

容器、网关、CDN、对象存储任何一层变更，都建议用 SpeedCE 从**外网多节点**验证。内网 curl 正常 ≠ 用户可访问。

工具：https://speedce.com/?lang=zh-CN

---

**SpeedCE** — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性  
官网：https://www.speedce.com | 中文：https://speedce.com/?lang=zh-CN | 联系：speedceads@gmail.com
