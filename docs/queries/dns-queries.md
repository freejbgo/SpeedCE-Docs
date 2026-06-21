# DNS 查询

被动 DNS 侦察用于发现 CDN CNAME 链与源站 A 记录，**不发送 HTTP 请求**。

实现：`leadminer/dns_lookup.py`

## CNAME 链查询

### 行为

对种子域名递归解析 CNAME，最多 **10 跳**，每跳检查是否匹配 CDN 指纹。

```python
chain, matches = await resolve_cname_chain("www.example.com", timeout=5.0)
# chain: ["www.example.com.cdn.cloudflare.net", ...]
# matches: [CdnMatch(vendor="Cloudflare", source="dns", detail="...")]
```

### 等效命令行（调试用）

```bash
# 查看完整 CNAME 链
dig +short CNAME www.example.com

# 跟踪 CNAME 直到 A 记录
dig +trace www.example.com

# 仅看最终 CNAME 目标
dig +short www.example.com CNAME
```

### 输出字段

| 字段 | 说明 |
|------|------|
| `cname_chain` | 完整 CNAME 链（pipeline 输出为 `\|` 分隔） |
| `cdn_evidence` | DNS 匹配详情，如 `www.example.cdn.cloudflare.net` |

### 超时与异常

| 情况 | 处理 |
|------|------|
| NXDOMAIN | 链为空，继续 HTTP 探测 |
| NoAnswer | 无 CNAME，链结束 |
| 超时（默认 5s） | 中断链解析 |
| 超过 10 跳 | 停止，防止环路 |

---

## A 记录查询

### 行为

解析域名 IPv4 A 记录，辅助判断源站位置（可结合 IPinfo 等外部服务）。

```python
ips = await resolve_a_records("example.com", timeout=5.0)
# ips: ["93.184.216.34"]
```

### 等效命令行

```bash
dig +short example.com A
```

### 输出字段

| 字段 | 说明 |
|------|------|
| `a_records` | IPv4 列表（pipeline 输出为 `\|` 分隔） |

---

## CDN 指纹匹配（DNS 侧）

CNAME 后缀与厂商映射见 [CDN 指纹库](cdn-fingerprints.md#dns-cname-后缀)。

匹配逻辑（`match_cname()`）：

- 将 CNAME 转小写并去掉末尾 `.`
- 若 `endswith(suffix)` 或 `suffix in cname` 则命中

**示例**：

| CNAME | 识别为 |
|-------|--------|
| `d111111abcdef8.cloudfront.net` | AWS CloudFront |
| `example.com.cdn.cloudflare.net` | Cloudflare |
| `example.b-cdn.net` | BunnyCDN |

---

## 在 Pipeline 中的位置

```
种子域名
  ├─ resolve_cname_chain()  → dns_vendors, cname_chain
  ├─ resolve_a_records()    → a_records
  └─ probe_domain()         → HTTP 侧 CDN（并行在同域名任务内顺序执行）
```

DNS 与 HTTP 发现的 CDN 厂商会 **合并去重** 写入 `cdn_vendors`。

---

## 扩展：历史 DNS（外部查询）

若需判断「是否刚换 CDN」，可使用商业 API：

| 服务 | 查询内容 |
|------|----------|
| [SecurityTrails](https://securitytrails.com/) | 历史 DNS 记录 |
| [IPinfo](https://ipinfo.io/) | IP → ASN / 机房 |

适合 enrichment 阶段，不建议对全量种子调用。
