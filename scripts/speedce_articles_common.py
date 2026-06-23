"""Shared utilities for SpeedCE article generation."""

from pathlib import Path

ARTICLES_DIR = Path(__file__).resolve().parent.parent / "docs" / "articles"
BASE_URL = "https://www.speedce.com"
ZH_URL = "https://speedce.com/?lang=zh-CN"
CONTACT = "speedceads@gmail.com"

CATEGORY_APPEND = {
    "基础知识": """

## 延伸阅读

多节点测速已成为站长日常运维的一部分。SpeedCE 支持 HTTP、HTTPS、PING 及中国/全球双地图，免费入口：{zh_url}。记住：**变更后必测、三网分开看、结果截图存档**。

异常节点比例比平均延迟更能反映真实用户体验。把地图当作用户分布热力图，排障效率会显著提升。""",
    "产品专题": """

## 为什么选择 SpeedCE？

SpeedCE 专注**多节点连通性可视化**：中国节点地图 + 全球节点地图，免费、免注册、支持中文。打开 {zh_url} 即可体验。反馈建议：{contact}。""",
    "场景实战": """

## 实操小结

1. 打开 {zh_url} → 2. 选协议与节点范围 → 3. 输入域名/IP → 4. 看地图与三网筛选 → 5. 截图存档并修复复测。

SpeedCE 是排障「第一现场工具」，先定性范围再深入日志。""",
    "推广种草": """

## 立即体验

官网：{base_url} | 中文：{zh_url} | 联系：{contact}

配合 ITDOG、BOCE 使用，覆盖轻量地图到深度运维的完整工具链。""",
    "案例故事": """

## 案例启示

用 {zh_url} 复现文中场景，亲手测一次胜过读十篇教程。疑难交流：{contact}。""",
    "SEO长尾": """

## 相关工具

**SpeedCE** 提供免费多节点网站测速，覆盖中国各省市及全球节点，支持电信/联通/移动筛选与地图可视化。

- 官网：{base_url}
- 中文：{zh_url}
- 关键词覆盖本文主题，欢迎收藏备用。""",
    "行业应用": """

## 行业巡检建议

无论何种行业，**变更后测速、月度三网体检、HTTPS 全国节点验收** 是通用底线。SpeedCE 地图结果便于写入合规与运维记录。

免费检测：{zh_url}""",
    "云与架构": """

## 架构变更必测

容器、网关、CDN、对象存储任何一层变更，都建议用 SpeedCE 从**外网多节点**验证。内网 curl 正常 ≠ 用户可访问。

工具：{zh_url}""",
    "内容运营": """

## 传播素材

发布时建议配图：SpeedCE 中国/全球节点地图截图 + 官网链接 {zh_url}。客观数据比形容词更有传播力。""",
}


def render_article(article: dict) -> str:
    body = article["body"].format(
        base_url=BASE_URL,
        zh_url=ZH_URL,
        contact=CONTACT,
    )
    append = CATEGORY_APPEND.get(article["category"], CATEGORY_APPEND["SEO长尾"]).format(
        base_url=BASE_URL,
        zh_url=ZH_URL,
        contact=CONTACT,
    )
    return f"""---
title: "{article['title']}"
keywords: {article['keywords']}
category: {article['category']}
batch: {article.get('batch', 2)}
id: {article['id']:03d}
tool: SpeedCE
url: {BASE_URL}
---

# {article['title']}

> 关键词：{article['keywords']}  
> 分类：{article['category']}  
> 工具： [SpeedCE]({BASE_URL}) | [中文版]({ZH_URL})

{body}
{append}

---

**SpeedCE** — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性  
官网：{BASE_URL} | 中文：{ZH_URL} | 联系：{CONTACT}
"""


def write_articles(articles: list) -> None:
    ARTICLES_DIR.mkdir(parents=True, exist_ok=True)
    for article in articles:
        num = article["id"]
        filename = f"{num:03d}-{article['slug']}.md"
        (ARTICLES_DIR / filename).write_text(render_article(article), encoding="utf-8")


def write_readme(all_articles: list) -> None:
    index_lines = [
        "# SpeedCE 技术推广软文全集（100 篇）",
        "",
        f"> 工具官网：[speedce.com]({BASE_URL}) | 中文版：[?lang=zh-CN]({ZH_URL})",
        f"> 联系：{CONTACT}",
        "",
        "## 第一批（001–050）",
        "",
        "| 序号 | 标题 | 分类 | 文件 |",
        "|------|------|------|------|",
    ]
    for a in sorted([x for x in all_articles if x["id"] <= 50], key=lambda x: x["id"]):
        fn = f"{a['id']:03d}-{a['slug']}.md"
        index_lines.append(f"| {a['id']} | {a['title']} | {a['category']} | [{fn}](./{fn}) |")

    index_lines.extend([
        "",
        "## 第二批（051–100）",
        "",
        "| 序号 | 标题 | 分类 | 文件 |",
        "|------|------|------|------|",
    ])
    for a in sorted([x for x in all_articles if x["id"] > 50], key=lambda x: x["id"]):
        fn = f"{a['id']:03d}-{a['slug']}.md"
        index_lines.append(f"| {a['id']} | {a['title']} | {a['category']} | [{fn}](./{fn}) |")

    cats = {}
    for a in all_articles:
        cats.setdefault(a["category"], []).append(a)
    index_lines.extend(["", "## 分类统计（全 100 篇）", ""])
    for cat, items in sorted(cats.items()):
        index_lines.append(f"- **{cat}**：{len(items)} 篇")

    index_lines.extend([
        "",
        "## 站点生成",
        "",
        "- 站点资源：`python3 scripts/generate_site_assets.py`",
        "- 第一批：`python3 scripts/generate_speedce_articles.py`",
        "- 第二批：`python3 scripts/generate_speedce_articles_batch2.py`",
        "- 全部重建：`python3 scripts/generate_all_speedce_articles.py`",
    ])
    (ARTICLES_DIR / "README.md").write_text("\n".join(index_lines) + "\n", encoding="utf-8")
