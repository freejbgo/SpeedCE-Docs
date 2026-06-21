# 线索筛选查询

Pipeline 导出 `data/leads/leads.csv` 后，用以下查询筛选高价值线索或竞品迁移机会。

## 基础查看

```bash
# 表格化查看（按 score 已降序）
column -s, -t < data/leads/leads.csv | head -30

# 统计各 tier 数量
awk -F, 'NR>1 {print $2}' data/leads/leads.csv | sort | uniq -c
```

## 按分级筛选

```bash
# 仅 hot
awk -F, '$2=="hot"' data/leads/leads.csv

# warm 及以上（hot + warm）
awk -F, 'NR==1 || $2=="hot" || $2=="warm"' data/leads/leads.csv
```

## 按 CDN 厂商筛选

`cdn_vendors` 列为 `|` 分隔的多厂商字符串。

```bash
# 使用 Cloudflare 的线索
awk -F, 'NR==1 || $9 ~ /Cloudflare/' data/leads/leads.csv

# 未检测到 CDN（增量市场）
awk -F, 'NR==1 || $9==""' data/leads/leads.csv

# AWS CloudFront 且 TTFB 慢（第 8 列 ttfb_ms >= 800）
awk -F, 'NR==1 || ($9 ~ /AWS CloudFront/ && $8+0 >= 800)' data/leads/leads.csv
```

## 竞品迁移机会（推荐组合）

| 筛选条件 | 业务含义 | 查询思路 |
|----------|----------|----------|
| `Cloudflare` + `ttfb_ms >= 800` | 大厂 CDN 但慢 | `$9 ~ /Cloudflare/ && $8+0 >= 800` |
| `AWS CloudFront` + `slow_ttfb` | 可谈副线路/迁移 | `$9 ~ /AWS CloudFront/` + score_reasons |
| 空 `cdn_vendors` + `asset_count_hint >= 8` | 无 CDN 但资源多 | `$9=="" && $11+0 >= 8` |
| `no_https` | 基础架构待优化 | score_reasons 含 `no_https` |

### 无 CDN + 高静态资源

```bash
awk -F, 'NR==1 || ($9=="" && $11+0 >= 8)' data/leads/leads.csv > data/leads/no_cdn_high_assets.csv
```

### 慢 TTFB 的 Cloudflare 客户

```bash
awk -F, 'NR==1 || ($9 ~ /Cloudflare/ && $8+0 >= 800)' data/leads/leads.csv \
  > data/leads/cf_slow.csv
```

## 按评分原因筛选

`score_reasons` 列含 `|` 分隔的信号，如 `no_cdn_detected (+20)|slow_ttfb=920ms (+15)`。

```bash
# 含 slow_ttfb 信号
awk -F, 'NR==1 || $15 ~ /slow_ttfb/' data/leads/leads.csv

# 含 no_cdn_detected
awk -F, 'NR==1 || $15 ~ /no_cdn_detected/' data/leads/leads.csv
```

## CSV 列索引参考

| 列号 | 字段 |
|------|------|
| 1 | `domain` |
| 2 | `tier` |
| 3 | `score` |
| 4 | `tranco_rank` |
| 5 | `source` |
| 6 | `reachable` |
| 7 | `status` |
| 8 | `ttfb_ms` |
| 9 | `cdn_vendors` |
| 10 | `uses_https` |
| 11 | `asset_count_hint` |
| 12 | `final_url` |
| 13 | `cname_chain` |
| 14 | `a_records` |
| 15 | `score_reasons` |
| 16 | `cdn_evidence` |
| 17 | `error` |

## Python 筛选示例

```python
import csv
from pathlib import Path

rows = list(csv.DictReader(Path("data/leads/leads.csv").open()))
hot_cf_slow = [
    r for r in rows
    if r["tier"] in ("hot", "warm")
    and "Cloudflare" in r["cdn_vendors"]
    and float(r["ttfb_ms"] or 0) >= 800
]
for r in hot_cf_slow[:10]:
    print(r["domain"], r["score"], r["ttfb_ms"], r["cdn_vendors"])
```

## 导出 JSON 后查询

```bash
python -m leadminer.cli run seeds.csv -o leads.csv --json data/leads/leads.json
```

```bash
# jq：hot 且使用 Akamai
jq '[.[] | select(.tier=="hot" and (.cdn_vendors | index("Akamai")))]' data/leads/leads.json
```

## 多地延迟合并（扩展）

在多台 VPS 各跑同一批种子，合并 `ttfb_ms`：

```bash
# 假设 leads-us.csv、leads-sg.csv、leads-eu.csv
# 若某域在目标区域明显慢于竞品 CDN → 标记 target_regions_slow 重新评分
```

可用 [GlobalPing](https://www.jsdelivr.com/network/globalping) 从多地域发起 HTTP 探测。

## CRM 导入字段建议

导出筛选结果时保留：

`domain`, `tier`, `score`, `cdn_vendors`, `ttfb_ms`, `asset_count_hint`, `score_reasons`

导入 Notion / Airtable / HubSpot 后追加：`contact_email`, `status`, `next_followup`
