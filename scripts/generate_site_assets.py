#!/usr/bin/env python3
"""Generate sitemap.xml, robots.txt, and article navigation data for GitHub Pages."""

from pathlib import Path
import re
import yaml

DOCS_DIR = Path(__file__).resolve().parent.parent / "docs"
ARTICLES_DIR = DOCS_DIR / "articles"
BASE_URL = "https://freejbgo.github.io/SpeedCE-Docs"


def parse_front_matter(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}
    end = text.find("---", 3)
    if end == -1:
        return {}
    try:
        return yaml.safe_load(text[3:end]) or {}
    except yaml.YAMLError:
        return {}


def collect_articles() -> list[dict]:
    articles = []
    for path in sorted(ARTICLES_DIR.glob("*.md")):
        if path.name == "README.md":
            continue
        meta = parse_front_matter(path)
        slug = path.stem
        article_id = meta.get("id", slug[:3])
        articles.append({
            "id": str(article_id).zfill(3) if str(article_id).isdigit() else str(article_id),
            "slug": slug,
            "title": meta.get("title", slug),
            "category": meta.get("category", ""),
            "url": f"/articles/{slug}.html",
        })
    articles.sort(key=lambda a: a["id"])
    return articles


def write_sitemap(articles: list[dict]) -> None:
    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">',
        f"  <url><loc>{BASE_URL}/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>",
        f"  <url><loc>{BASE_URL}/articles/</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>",
    ]
    for a in articles:
        lines.append(
            f"  <url><loc>{BASE_URL}{a['url']}</loc>"
            f"<changefreq>monthly</changefreq><priority>0.7</priority></url>"
        )
    lines.append("</urlset>")
    (DOCS_DIR / "sitemap.xml").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_robots() -> None:
    content = f"""User-agent: *
Allow: /

Sitemap: {BASE_URL}/sitemap.xml
"""
    (DOCS_DIR / "robots.txt").write_text(content, encoding="utf-8")


def write_article_nav(articles: list[dict]) -> None:
    data_dir = DOCS_DIR / "_data"
    data_dir.mkdir(exist_ok=True)
    nav = {}
    for i, a in enumerate(articles):
        key = a["slug"].split("-")[0]
        entry = {}
        if i > 0:
            prev = articles[i - 1]
            entry["previous"] = {"title": prev["title"], "url": prev["url"]}
        if i < len(articles) - 1:
            nxt = articles[i + 1]
            entry["next"] = {"title": nxt["title"], "url": nxt["url"]}
        nav[key] = entry
    (data_dir / "article_nav.yml").write_text(
        yaml.dump(nav, allow_unicode=True, default_flow_style=False),
        encoding="utf-8",
    )


def write_category_index(articles: list[dict]) -> None:
    cats: dict[str, list] = {}
    for a in articles:
        cats.setdefault(a["category"] or "未分类", []).append(a)

    lines = [
        "---",
        "title: 文章分类索引",
        "layout: default",
        "permalink: /categories/",
        "---",
        "",
        "# 按分类浏览",
        "",
    ]
    for cat in sorted(cats.keys()):
        lines.append(f"## {cat}（{len(cats[cat])} 篇）")
        lines.append("")
        for a in cats[cat]:
            lines.append(f"- [{a['title']}]({a['url']})")
        lines.append("")

    (DOCS_DIR / "categories.md").write_text("\n".join(lines), encoding="utf-8")


def fix_readme_links() -> None:
    readme = ARTICLES_DIR / "README.md"
    text = readme.read_text(encoding="utf-8")
    text = re.sub(r"\]\(\./(\d{3}-[^)]+\.)md\)", r"](./\1html)", text)
    readme.write_text(text, encoding="utf-8")


if __name__ == "__main__":
    articles = collect_articles()
    write_sitemap(articles)
    write_robots()
    write_article_nav(articles)
    write_category_index(articles)
    fix_readme_links()
    print(f"Generated site assets for {len(articles)} articles")
