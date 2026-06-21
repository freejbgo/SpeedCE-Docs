# 工作流与触达

面向 **技术兼商务、零销售编制** 团队的推荐运营节奏与合规要点。

## 推荐周循环

```
周一  更新 Tranco 种子 5000 → 跑 pipeline → 导出 warm+
周二  按 cdn_vendors / tier 分组，人工筛 30 个
周三  BuiltWith/Hunter 补 10 个公司的技术联系人
周四  发 10 封技术向邮件 / Telegram（附 PoC 方案）
周五  跟进 2 个 PoC，把结果写成案例片段
```

### 周一：批量探测

```bash
python -m leadminer.cli fetch-tranco <LIST_ID> -n 5000 -o data/seeds/tranco.csv
python -m leadminer.cli run data/seeds/tranco.csv -o data/leads/leads.csv --min-tier warm
```

### 周二：人工复核

参考 [线索筛选查询](queries/lead-filters.md)：

- 优先 `hot` + `major_cdn` + `slow_ttfb`
- 排除明显不匹配的行业（政府、纯内容站等）
- 目标：留下约 30 条

### 周三：联系人 enrichment

| 工具 | 用途 |
|------|------|
| [Hunter.io](https://hunter.io/) | 按域名找技术邮箱 |
| [Snov.io](https://snov.io/) | 邮箱验证 |
| [BuiltWith](https://builtwith.com/) | 技术栈确认 |

### 周四：触达

见下方邮件模板。

### 周五：PoC 跟进

- 记录对比数据（TTFB、缓存命中率）
- 整理为 2–3 句案例片段供下次触达引用

---

## 邮件模板（技术向）

**主题**：`PoC offer: CDN latency check for {{domain}}`

**正文要点**：

- 我们注意到 `{{domain}}` 当前使用 `{{cdn_vendors}}`，首页 TTFB 约 `{{ttfb_ms}}`ms。
- 我们运营海外自营节点，可提供 **14 天免费并行 PoC**（不改主站，仅子域名测试）。
- 附迁移 checklist 与对比方法，无需销售电话。

**变量来源**：`data/leads/leads.csv` 对应列。

---

## 合规与边界（必读）

1. **只探测首页** `/`，遵守 robots.txt 精神；不扫路径、不爆破。
2. **速率限制**：默认并发 20，对单域名不要 repeated 探测。
3. **User-Agent** 标明身份与联系邮箱。
4. **数据最小化**：只存域名、CDN、延迟等 B2B 公开技术事实；不爬个人隐私。
5. **触达合规**：邮件需退订；欧盟注意 GDPR；境外客户注意 CAN-SPAM 等。
6. **用途限制**：不用于灰产、钓鱼、未授权渗透。

---

## 多地延迟探测（扩展）

从单节点探测只能反映一个地理视角。证明「你的 CDN 在目标市场更快」：

1. 在东南亚 / 美西 / 欧洲各放一台探测 VPS
2. 每台跑同一批种子或 leads
3. 合并 `ttfb_ms`；若竞品在 A 地快、目标地慢 → 提高 `target_regions_slow` 评分（+10）

工具：[GlobalPing](https://www.jsdelivr.com/network/globalping) 或自建 `probe.sh` + cron

---

## CRM 对接

导出 CSV 后导入：

| 工具 | 适用场景 |
|------|----------|
| Notion / Airtable | 免费、灵活 |
| HubSpot Free | 带邮件序列 |

**推荐字段**：

`domain`, `tier`, `cdn_vendors`, `ttfb_ms`, `contact_email`, `status`, `next_followup`

---

## 项目结构

```
leadminer/
  cdn_fingerprints.py   # CDN 指纹库
  dns_lookup.py         # CNAME / A 记录
  http_probe.py         # 首页探测
  scoring.py            # 线索评分
  pipeline.py           # 流水线
  seeds.py              # Tranco 种子
  cli.py                # 命令行
data/
  seeds/                # 输入域名
  leads/                # 输出线索
docs/
  queries/              # 查询文档
  cli-reference.md
  workflow.md
```
