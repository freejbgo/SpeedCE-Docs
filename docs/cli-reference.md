# CLI 命令参考

入口：`python -m leadminer.cli`

## 子命令一览

| 子命令 | 说明 |
|--------|------|
| `fetch-tranco` | 从 Tranco 下载 Top 域名种子 |
| `run` | 探测种子并导出评分线索 |

---

## fetch-tranco

下载 Tranco 全球流量 Top 列表为 CSV。

```bash
python -m leadminer.cli fetch-tranco <LIST_ID> [选项]
```

### 参数

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `list_id` | 是 | — | Tranco 列表 ID，见 https://tranco-list.eu/ |
| `-o`, `--output` | 否 | `data/seeds/tranco.csv` | 输出路径 |
| `-n`, `--limit` | 否 | `5000` | 最多下载条数 |

### 示例

```bash
# 下载 Top 1000
python -m leadminer.cli fetch-tranco L5VX9 -n 1000 -o data/seeds/tranco.csv

# 下载 Top 10000
python -m leadminer.cli fetch-tranco L5VX9 -n 10000 -o data/seeds/tranco_10k.csv
```

### 输出

```csv
domain,tranco_rank,source
google.com,1,tranco:L5VX9
```

---

## run

对种子文件执行 DNS + HTTP 探测、CDN 识别、评分，导出 CSV。

```bash
python -m leadminer.cli run <SEEDS> [选项]
```

### 参数

| 参数 | 必填 | 默认 | 说明 |
|------|------|------|------|
| `seeds` | 是 | — | 种子 CSV 或 `.txt` 路径 |
| `-o`, `--output` | 否 | `data/leads/leads.csv` | CSV 输出路径 |
| `--json` | 否 | — | 可选 JSON 输出路径 |
| `-c`, `--concurrency` | 否 | `20` | 并发数 |
| `--min-tier` | 否 | `cool` | 最低导出分级：`hot`/`warm`/`cool`/`low` |
| `--user-agent` | 否 | 内置默认值 | 自定义 User-Agent |

### 示例

```bash
# 基础运行
python -m leadminer.cli run data/seeds/example.csv -o data/leads/leads.csv

# 只导出 warm 及以上
python -m leadminer.cli run data/seeds/tranco.csv \
  -o data/leads/leads.csv \
  --min-tier warm

# 自定义 UA + JSON 导出 + 提高并发
python -m leadminer.cli run data/seeds/tranco.csv \
  -o data/leads/leads.csv \
  --json data/leads/leads.json \
  -c 30 \
  --user-agent "LeadMiner/0.1 (+mailto:ops@corp.com)" \
  --min-tier hot
```

### 终端输出示例

```
Probed 5000 domains; exported 342 (min_tier=warm) to data/leads/leads.csv
  hot=28 warm=314
```

### 种子格式

- **CSV**：需含 `domain` 列；可选 `tranco_rank`, `source`
- **TXT**：每行一个域名，`#` 为注释

---

## 完整工作流

```bash
pip install -r requirements.txt

# Step 1: 获取种子
python -m leadminer.cli fetch-tranco L5VX9 -n 5000 -o data/seeds/tranco.csv

# Step 2: 探测评分
python -m leadminer.cli run data/seeds/tranco.csv \
  -o data/leads/leads.csv \
  --min-tier warm \
  --user-agent "LeadMiner/0.1 (+mailto:you@corp.com)"

# Step 3: 查看结果
column -s, -t < data/leads/leads.csv | head -20
```

---

## 依赖

见项目根目录 `requirements.txt`：

```
aiohttp>=3.9.0
dnspython>=2.6.0
```

---

## 退出码

| 码 | 含义 |
|----|------|
| 0 | 成功 |
| 1 | 种子文件为空或未知子命令 |
