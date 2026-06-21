# 评分规则

根据 DNS/HTTP 探测结果计算线索分值，分为 `hot` / `warm` / `cool` / `low` / `skip`。

实现：`leadminer/scoring.py` → `score_lead()`

## 分值表

### Tranco 流量排名

| 排名 ≤ | 加分 |
|--------|------|
| 10,000 | +25 |
| 100,000 | +18 |
| 500,000 | +12 |
| 1,000,000 | +8 |
| 5,000,000 | +4 |
| 无排名 | 0 |

### CDN 状态

| 条件 | 加分 | 信号名 |
|------|------|--------|
| 未检测到任何 CDN | +20 | `no_cdn_detected` |
| 使用主流 CDN（见指纹库） | +12 | `major_cdn` |
| 使用小众 CDN | +6 | `niche_cdn` |

### 性能与架构

| 条件 | 加分 | 信号名 |
|------|------|--------|
| TTFB ≥ 800ms | +15 | `slow_ttfb` |
| TTFB 400–799ms | +8 | `moderate_ttfb` |
| 第三方静态资源 ≥ 8 | +10 | `many_third_party_assets` |
| 第三方静态资源 3–7 | +5 | `some_third_party_assets` |
| 未使用 HTTPS | +5 | `no_https` |
| 目标区域慢（手动标记） | +10 | `slow_in_target_region` |

### 不可达

| 条件 | 结果 |
|------|------|
| HTTP 探测失败 | `score=0`, `tier=skip` |

## 分级阈值

| Tier | 分值 ≥ | 建议动作 |
|------|--------|----------|
| `hot` | 45 | 优先触达 |
| `warm` | 28 | 人工复核后触达 |
| `cool` | 15 | 观察/批量跟进 |
| `low` | < 15 | 暂搁置 |
| `skip` | 0（不可达） | 丢弃 |

## 评分示例

### 示例 1：高价值线索（hot）

```
tranco_rank=5000        → +25
no_cdn_detected         → +20
slow_ttfb=920ms         → +15
many_third_party_assets=12 → +10
─────────────────────────
total = 70 → hot
```

### 示例 2：竞品迁移机会（warm）

```
tranco_rank=50000       → +18
major_cdn=Cloudflare    → +12
slow_ttfb=650ms         → +8
some_third_party_assets=5 → +5
─────────────────────────
total = 43 → warm（接近 hot）
```

### 示例 3：低优先级（cool）

```
niche_cdn=BunnyCDN      → +6
moderate_ttfb=450ms     → +8
─────────────────────────
total = 14 → low
```

## CLI 最低分级过滤

```bash
# 只导出 warm 及以上
python -m leadminer.cli run seeds.csv --min-tier warm

# 只导出 hot
python -m leadminer.cli run seeds.csv --min-tier hot
```

Tier 顺序：`hot(3) > warm(2) > cool(1) > low(0)`

## 调整权重

直接修改 `leadminer/scoring.py`：

```python
RANK_TIERS = [
    (10_000, 25),   # 可调流量权重
    ...
]

# 分级阈值
if score >= 45: tier = "hot"   # 可调
elif score >= 28: tier = "warm"
```

## 运营建议

- 每周只跟进 **hot** + 前 **20** 条 **warm**
- `cool` 进入观察池，等 Tranco 排名上升或 CDN 变更后再评估
- 对 `major_cdn` + `slow_ttfb` 组合优先写「并行 PoC」话术
