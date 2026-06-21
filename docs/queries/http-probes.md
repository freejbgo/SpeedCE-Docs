# HTTP 探测查询

轻量主动探测：仅请求首页 `/`，采集 TTFB、响应头、静态资源线索。

实现：`leadminer/http_probe.py`

## 探测流程

```
1. 规范化域名（去协议、路径、转小写）
2. 尝试 HTTPS GET https://{domain}/
3. 失败则回退 HTTP GET http://{domain}/
4. 采集：status, ttfb_ms, headers, body 前 200KB
5. 匹配 HTTP CDN 指纹 + 统计第三方静态资源
```

## 请求参数

| 参数 | 默认 | 说明 |
|------|------|------|
| `timeout` | 10s | 总请求超时 |
| `user_agent` | `LeadMiner/0.1 (...)` | 可通过 CLI `--user-agent` 覆盖 |
| `allow_redirects` | `true` | 跟随重定向 |
| `max_line_size` | 16384 | 响应行大小上限 |
| `max_field_size` | 16384 | 响应头字段大小上限 |

### 推荐 User-Agent

```bash
python -m leadminer.cli run seeds.csv \
  --user-agent "LeadMiner/0.1 (+mailto:ops@yourcompany.com)"
```

## 采集指标

| 指标 | 字段 | 说明 |
|------|------|------|
| 可达性 | `ok` / `reachable` | HTTPS 或 HTTP 至少一个成功 |
| HTTP 状态 | `status` | 最终响应码 |
| 首字节时间 | `ttfb_ms` | 从发起到收到首字节的毫秒数 |
| 总耗时 | `total_ms` | 含 body 下载 |
| 最终 URL | `final_url` | 重定向后地址 |
| HTTPS | `uses_https` | 最终 URL 是否为 https |
| 响应头 | `headers` | 完整头（JSON 导出时可见） |
| CDN 厂商 | `cdn_vendors` | HTTP 头匹配结果 |
| CDN 证据 | `cdn_evidence` | 如 `cf-ray: abc123` |
| 第三方资源 | `asset_count_hint` | 首页引用的外部域静态资源数 |

## TTFB 阈值（评分用）

| TTFB | 评分信号 |
|------|----------|
| ≥ 800ms | `slow_ttfb` +15 分 |
| 400–799ms | `moderate_ttfb` +8 分 |
| < 400ms | 不加分 |

## 静态资源计数规则

扫描 HTML 中 `<script>`, `<link>`, `<img>`, `<source>` 的 `src`/`href`：

- 跳过 `data:`, `javascript:`, `#` 链接
- 统计 **host 与当前页不同** 的绝对 URL 数量
- 仅解析 body 前 **200,000** 字符

**含义**：`asset_count_hint >= 8` 表示第三方静态资源较多，适合 CDN 加速（+10 分）。

## 等效 curl 调试

```bash
# 测 TTFB 与响应头
curl -o /dev/null -s -w "ttfb=%{time_starttransfer}s status=%{http_code}\n" \
  -H "User-Agent: LeadMiner/0.1" \
  https://example.com/

# 查看 CDN 相关头
curl -sI https://example.com/ | grep -iE 'cf-ray|x-amz|x-cache|x-served-by|server'
```

## 失败处理

| 情况 | `error` 字段 |
|------|--------------|
| HTTPS 和 HTTP 均失败 | `https and http both failed` |
| 超时 | 尝试下一协议，均失败同上 |
| SSL 错误 | 连接器 `ssl=False`，仍尝试 HTTP |

不可达域名在评分阶段标记为 `tier=skip`。

## 合规边界

1. **只探测** `/`，不扫子路径
2. 遵守 robots.txt 精神，不做深度爬取
3. 默认并发 20，避免对单域 repeated 探测
4. User-Agent 须标明身份与联系方式
