# 种子来源查询

域名种子是后续 DNS/HTTP 查询的输入。按 **性价比** 与 **精准度** 分为四类。

## A. 流量榜单（广撒网）

### Tranco Top 列表

**用途**：获取全球有流量的站点，适合批量拓客。

**查询方式**（内置 CLI）：

```bash
# list_id 从 https://tranco-list.eu/ 获取，每日更新
python -m leadminer.cli fetch-tranco L5VX9 -n 5000 -o data/seeds/tranco.csv
```

**底层 API**：

```
GET https://tranco-list.eu/download/{list_id}/1000000
```

实现：`leadminer/seeds.py` → `fetch_tranco_top()`

| 参数 | 说明 | 默认 |
|------|------|------|
| `list_id` | Tranco 列表 ID | 必填 |
| `-n` / `--limit` | 最多取多少条 | 5000 |
| `-o` / `--output` | 输出 CSV 路径 | `data/seeds/tranco.csv` |

**输出示例**：

```csv
domain,tranco_rank,source
google.com,1,tranco:L5VX9
youtube.com,2,tranco:L5VX9
```

### Cloudflare Radar Top Domains

**用途**：按国家/行业筛选高流量域（需注册 API）。

**查询方式**（外部 API，需自行对接）：

- 文档：https://developers.cloudflare.com/radar/
- 适合与 Tranco 交叉验证或按区域定向

---

## B. 证书透明度（找新站、出海站）

### crt.sh 关键词查询

**用途**：发现含特定 TLD 或关键词的新证书域名（独立站、跨境电商）。

**查询示例**：

```bash
# 含 .shop 的证书域名（注意速率限制）
curl -s 'https://crt.sh/?q=%.shop&output=json' \
  | jq -r '.[].name_value' \
  | sort -u \
  | head -500 \
  > data/seeds/shop.txt
```

**常用查询模式**：

| 查询 URL | 场景 |
|----------|------|
| `https://crt.sh/?q=%.shop&output=json` | 独立站 / 电商 |
| `https://crt.sh/?q=%.io&output=json` | 科技/SaaS 新站 |
| `https://crt.sh/?q=%.app&output=json` | 应用类产品 |
| `https://crt.sh/?q=%25.example.com&output=json` | 某主域的子域枚举 |

**注意**：

- crt.sh 有速率限制，建议 `head` 限制数量并加延时
- 输出需去重（`sort -u`），证书常含通配符 `*.domain.com`
- 转为 pipeline 输入：保存为 `.txt`（每行一域）或整理为 CSV

**后处理为 CSV**：

```bash
awk '{print $0 ",,crt.sh:shop"}' data/seeds/shop.txt > data/seeds/shop.csv
# 需补 header: domain,tranco_rank,source
```

---

## C. 垂直行业目录（精准）

手动或脚本整理为 CSV，格式：`domain,tranco_rank,source`

| 行业 | 数据来源 | 备注 |
|------|----------|------|
| 独立站 | Shopify 案例页、Product Hunt、Indie Hackers | 高转化 |
| 游戏 | itch.io、Steam 开发商官网、Discord 社群 | 静态资源多 |
| SaaS | G2、Capterra 小厂商官网 | 技术决策人明确 |
| 直播/视频 | 合规平台主播独立站 | 延迟敏感 |

**示例 CSV**：

```csv
domain,tranco_rank,source
coolstartup.io,,producthunt:2024-06
indiegame.dev,,itch.io
```

---

## D. 竞品客户（从已有线索反查）

对 `data/leads/leads.csv` 按 CDN 厂商与性能信号筛选，见 [线索筛选查询](lead-filters.md)。

典型组合：

- `Cloudflare` + `slow_ttfb` → 价格/服务痛点
- `no_cdn_detected` + 高 `asset_count_hint` → 静态加速需求

---

## 种子预过滤

在探测前用 `filter_domains()` 减少无效查询（`leadminer/seeds.py`）：

```python
from leadminer.seeds import filter_domains

filtered = filter_domains(
    rows,
    include_tlds=["com", "io", "shop"],      # 只保留这些 TLD
    exclude_tlds=["gov", "edu", "mil"],      # 排除政府/教育
    exclude_vendors=["Cloudflare"],          # 排除已知某 CDN 的域
    cdn_map={"example.com": ["Cloudflare"]}, # 来自历史探测结果
)
```

| 参数 | 作用 |
|------|------|
| `include_tlds` | 白名单 TLD |
| `exclude_tlds` | 黑名单 TLD |
| `exclude_vendors` | 跳过已知使用某 CDN 的域名 |
| `cdn_map` | `domain → [vendors]` 映射 |

---

## 推荐组合策略

| 目标 | 种子来源 | 建议数量 |
|------|----------|----------|
| 周更广撒网 | Tranco Top 5000 | 5000 |
| 独立站专项 | crt.sh `.shop` | 500 |
| 高精准 | 行业目录手动 | 50–100 |
| 竞品迁移 | 历史 leads 筛选 | 30 |
