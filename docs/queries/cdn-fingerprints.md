# CDN 指纹库

DNS CNAME 与 HTTP 响应头两套规则合并识别 CDN 厂商。

实现：`leadminer/cdn_fingerprints.py`

## DNS CNAME 后缀

| CNAME 后缀 | 厂商 |
|------------|------|
| `cloudflare.net` | Cloudflare |
| `cloudflare.com` | Cloudflare |
| `cloudfront.net` | AWS CloudFront |
| `akamaiedge.net` | Akamai |
| `akamaized.net` | Akamai |
| `edgesuite.net` | Akamai |
| `edgekey.net` | Akamai |
| `fastly.net` | Fastly |
| `fastlylb.net` | Fastly |
| `azureedge.net` | Azure CDN |
| `azurefd.net` | Azure Front Door |
| `googleusercontent.com` | Google Cloud CDN |
| `googlesyndication.com` | Google |
| `stackpathdns.com` | StackPath |
| `kxcdn.com` | KeyCDN |
| `b-cdn.net` | BunnyCDN |
| `cdn77.org` | CDN77 |
| `incapdns.net` | Imperva |
| `hwcdn.net` | Highwinds |
| `llnwi.net` | Limelight |
| `lswcdn.net` | Leaseweb CDN |
| `alicdn.com` | Alibaba CDN |
| `kunlun` | Alibaba CDN |
| `qcloud.com` | Tencent CDN |
| `myqcloud.com` | Tencent CDN |
| `wsdvs.com` | Verizon EdgeCast |
| `edgecastcdn.net` | Verizon EdgeCast |
| `netlify.com` | Netlify |
| `vercel-dns.com` | Vercel |
| `github.io` | GitHub Pages |
| `shopifycdn.com` | Shopify |

## HTTP 响应头规则

格式：`(header_name, regex_on_value, vendor)`

| Header | 匹配规则 | 厂商 |
|--------|----------|------|
| `server` | 含 `cloudflare` | Cloudflare |
| `cf-ray` | 任意非空 | Cloudflare |
| `cf-cache-status` | 任意非空 | Cloudflare |
| `x-served-by` | 含 `cache-` | Fastly |
| `x-cache` | 含 `fastly` | Fastly |
| `x-fastly-request-id` | 任意非空 | Fastly |
| `x-amz-cf-id` | 任意非空 | AWS CloudFront |
| `x-amz-cf-pop` | 任意非空 | AWS CloudFront |
| `x-cache` | 含 `cloudfront` | AWS CloudFront |
| `x-akamai-*` | 前缀匹配，值非空 | Akamai |
| `x-ecdn` | 任意非空 | Azure CDN |
| `x-azure-ref` | 任意非空 | Azure CDN |
| `via` | 含 `google` | Google Cloud CDN |
| `x-cdn` | 任意非空 | Generic CDN |
| `x-cdn-pop` | 任意非空 | Generic CDN |
| `x-edge-location` | 任意非空 | Generic CDN |
| `x-bunny-*` | 前缀匹配 | BunnyCDN |
| `x-keycdn` | 任意非空 | KeyCDN |

> 注：`x-akamai-*`、`x-bunny-*` 使用前缀匹配，会扫描所有以该前缀开头的响应头。

## 主流 CDN 厂商（竞品标记）

以下厂商在评分中视为 **major_cdn**（+12 分，可谈迁移/副线路）：

- Cloudflare
- AWS CloudFront
- Akamai
- Fastly
- Azure CDN
- Google Cloud CDN
- Alibaba CDN
- Tencent CDN

定义：`MAJOR_VENDORS` in `cdn_fingerprints.py`

## 快速识别对照（常用）

| 厂商 | DNS 特征 | HTTP 特征 |
|------|----------|-----------|
| Cloudflare | `*.cloudflare.net` | `cf-ray`, `server: cloudflare` |
| AWS CloudFront | `*.cloudfront.net` | `x-amz-cf-id`, `x-cache: cloudfront` |
| Fastly | `*.fastly.net` | `x-served-by: cache-`, `x-fastly-request-id` |
| Akamai | `*.akamaiedge.net` | `x-akamai-*` |
| BunnyCDN | `*.b-cdn.net` | `x-bunny-*` |

## 合并逻辑

1. DNS CNAME 链每跳调用 `match_cname()`
2. HTTP 响应头调用 `match_headers()`
3. `consolidate_matches()` 按厂商名去重
4. Pipeline 将 DNS + HTTP 结果合并为 `cdn_vendors`

## 扩展指纹

在 `leadminer/cdn_fingerprints.py` 中追加：

```python
# DNS
CNAME_PATTERNS.append(("your-cdn.net", "Your CDN"))

# HTTP
HEADER_PATTERNS.append(("x-your-cdn", r".+", "Your CDN"))
```

## 第三方商业指纹（可选）

| 服务 | 用途 |
|------|------|
| [BuiltWith](https://builtwith.com/) | 技术栈 + CDN API |
| [Wappalyzer](https://www.wappalyzer.com/) | 技术栈检测 API |

适合对 **warm/hot** 线索做 enrichment，不建议全量种子调用。
