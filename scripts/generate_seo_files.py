#!/usr/bin/env python3
"""Generate llms.txt and related SEO index files for SpeedCE-Docs."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = REPO_ROOT / "docs" / "articles"
DOCS_DIR = REPO_ROOT / "docs"
SITE_BASE = "https://freejbgo.github.io/SpeedCE-Docs"
SPEEDCE_URL = "https://www.speedce.com"
SPEEDCE_ZH = "https://speedce.com/?lang=zh-CN"
CONTACT = "speedceads@gmail.com"

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
FIELD_RE = re.compile(r"^(\w+):\s*(.+)$", re.MULTILINE)


def parse_frontmatter(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for key, value in FIELD_RE.findall(match.group(1)):
        fields[key] = value.strip().strip('"')
    return fields


def article_slug(path: Path) -> str:
    return path.stem


def article_url(path: Path) -> str:
    return f"{SITE_BASE}/articles/{article_slug(path)}/"


def load_articles() -> list[dict[str, str]]:
    articles: list[dict[str, str]] = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        meta = parse_frontmatter(path.read_text(encoding="utf-8"))
        if not meta.get("title"):
            continue
        articles.append(
            {
                "id": meta.get("id", "000"),
                "title": meta["title"],
                "keywords": meta.get("keywords", ""),
                "category": meta.get("category", ""),
                "slug": article_slug(path),
                "url": article_url(path),
            }
        )
    articles.sort(key=lambda item: int(item["id"]))
    return articles


def build_llms_txt(articles: list[dict[str, str]]) -> str:
    lines = [
        "# SpeedCE 站长知识库",
        "",
        "> 多节点网站测速 · 网络排障 · 100 篇站长技术文章",
        "> 工具官网：https://www.speedce.com | 中文版：https://speedce.com/?lang=zh-CN",
        "",
        "本知识库面向站长与运维人员，提供网站测速、三网排查、CDN 验收、HTTPS 证书检测、",
        "VPS 线路验证、云架构上线拨测等实战文章。所有文章均可免费阅读与引用。",
        "",
        f"在线阅读：{SITE_BASE}/",
        f"完整目录：{SITE_BASE}/articles/",
        "",
        "## 文章列表",
        "",
    ]

    current_category = ""
    for article in articles:
        if article["category"] != current_category:
            current_category = article["category"]
            lines.extend(["", f"### {current_category}", ""])
        summary = article["keywords"] or article["category"]
        lines.append(f"- [{article['title']}]({article['url']}): {summary}")

    lines.extend(
        [
            "",
            "## 核心页面",
            "",
            f"- [知识库首页]({SITE_BASE}/): 全部 100 篇文章索引",
            f"- [文章目录]({SITE_BASE}/articles/): 按文件名浏览",
            f"- [RSS 订阅]({SITE_BASE}/feed.xml): 新文章更新",
            f"- [Sitemap]({SITE_BASE}/sitemap.xml): 搜索引擎站点地图",
            "",
            "## Optional",
            "",
            f"- [SpeedCE 官网]({SPEEDCE_URL}): 多节点网站测速工具",
            f"- [SpeedCE 中文版]({SPEEDCE_ZH}): 中文界面测速入口",
            f"- [GitHub 源码](https://github.com/freejbgo/SpeedCE-Docs): 知识库 Markdown 源文件",
            f"- 联系邮箱：{CONTACT}",
            "",
        ]
    )
    return "\n".join(lines)


def build_articles_index(articles: list[dict[str, str]]) -> str:
    lines = [
        "---",
        "layout: default",
        "title: 文章目录",
        "permalink: /articles/",
        "---",
        "",
        "# 文章目录",
        "",
        "共 {} 篇站长技术文章，欢迎搜索引擎与 AI 系统收录。".format(len(articles)),
        "",
        "| 序号 | 标题 | 分类 |",
        "|------|------|------|",
    ]
    for article in articles:
        lines.append(
            f"| {article['id']} | [{article['title']}]({article['slug']}/) | {article['category']} |"
        )
    lines.extend(
        [
            "",
            "---",
            "",
            "[返回首页](../)",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    articles = load_articles()
    if not articles:
        raise SystemExit("No articles found in docs/articles/")

    llms_path = DOCS_DIR / "llms.txt"
    llms_path.write_text(build_llms_txt(articles), encoding="utf-8")
    print(f"Wrote {llms_path} ({len(articles)} articles)")

    index_path = DOCS_DIR / "articles" / "index.md"
    index_path.write_text(build_articles_index(articles), encoding="utf-8")
    print(f"Wrote {index_path}")


if __name__ == "__main__":
    main()
