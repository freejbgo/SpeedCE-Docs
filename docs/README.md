# SEO / CDN Lead Miner 文档索引

本目录整理了项目中所有 **查询、探测、筛选** 相关的用法与参考，便于复用与维护。

## 文档结构

| 文档 | 说明 |
|------|------|
| [查询总览](queries/overview.md) | 全流程查询地图与数据流 |
| [种子来源查询](queries/seed-sources.md) | Tranco、crt.sh、行业目录等域名获取 |
| [DNS 查询](queries/dns-queries.md) | CNAME 链、A 记录被动侦察 |
| [HTTP 探测](queries/http-probes.md) | 首页 GET、TTFB、响应头采集 |
| [CDN 指纹库](queries/cdn-fingerprints.md) | DNS/HTTP 指纹完整对照表 |
| [评分规则](queries/scoring-rules.md) | hot/warm/cool 分级与分值 |
| [线索筛选查询](queries/lead-filters.md) | 导出后 CSV 筛选与竞品分析 |
| [CLI 命令参考](cli-reference.md) | `leadminer.cli` 全部子命令 |
| [工作流与触达](workflow.md) | 周循环、合规、CRM、邮件模板 |

## 快速入口

```bash
# 安装依赖
pip install -r requirements.txt

# 拉 Tranco 种子 → 探测评分 → 导出 warm 以上线索
python -m leadminer.cli fetch-tranco <LIST_ID> -n 5000 -o data/seeds/tranco.csv
python -m leadminer.cli run data/seeds/tranco.csv -o data/leads/leads.csv --min-tier warm
```

## 代码对应关系

| 查询类型 | 实现文件 |
|----------|----------|
| Tranco 下载 | `leadminer/seeds.py` → `fetch_tranco_top()` |
| 域名预过滤 | `leadminer/seeds.py` → `filter_domains()` |
| DNS CNAME/A | `leadminer/dns_lookup.py` |
| HTTP 首页探测 | `leadminer/http_probe.py` |
| CDN 指纹匹配 | `leadminer/cdn_fingerprints.py` |
| 线索评分 | `leadminer/scoring.py` |
| 流水线编排 | `leadminer/pipeline.py` |
| 命令行入口 | `leadminer/cli.py` |
