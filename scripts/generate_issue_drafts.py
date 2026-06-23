#!/usr/bin/env python3
"""Generate GitHub Issue drafts from SpeedCE knowledge-base articles."""

from __future__ import annotations

import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
ARTICLES_DIR = REPO_ROOT / "docs" / "articles"
DRAFTS_DIR = REPO_ROOT / "docs" / "issue-drafts"
GITHUB_REPO = "freejbgo/SpeedCE-Docs"
GITHUB_BRANCH = "main"
BASE_URL = "https://www.speedce.com"
ZH_URL = "https://speedce.com/?lang=zh-CN"

# Category append headings appended during article generation — strip for Issue body.
APPEND_HEADINGS = (
    "## 延伸阅读",
    "## 为什么选择 SpeedCE",
    "## 实操小结",
    "## 立即体验",
    "## 案例启示",
    "## 相关工具",
    "## 行业巡检建议",
    "## 架构变更必测",
    "## 传播素材",
)

FOOTER_PATTERN = re.compile(
    r"\n---\n\n\*\*SpeedCE\*\* — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性\n"
    r"官网：.*\n?",
    re.MULTILINE,
)


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    if not text.startswith("---"):
        return {}, text
    end = text.find("\n---", 3)
    if end == -1:
        return {}, text
    block = text[3:end].strip()
    meta: dict[str, str] = {}
    for line in block.splitlines():
        if ":" in line:
            key, _, value = line.partition(":")
            meta[key.strip()] = value.strip().strip('"')
    return meta, text[end + 4 :].lstrip("\n")


def strip_issue_body(content: str) -> str:
    """Remove SEO meta, category append, and footer from article markdown."""
    content = FOOTER_PATTERN.sub("", content)

    cut = len(content)
    for heading in APPEND_HEADINGS:
        idx = content.find(f"\n{heading}")
        if idx != -1:
            cut = min(cut, idx)
    content = content[:cut]

    lines = content.splitlines()
    cleaned: list[str] = []
    skip_blockquote = False
    for line in lines:
        if line.startswith("# ") and not cleaned:
            continue
        if line.startswith("> "):
            skip_blockquote = True
            continue
        if skip_blockquote and line.strip() == "":
            skip_blockquote = False
            continue
        if skip_blockquote:
            continue
        cleaned.append(line)

    body = "\n".join(cleaned).strip()
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body


def article_github_url(filename: str) -> str:
    return (
        f"https://github.com/{GITHUB_REPO}/blob/{GITHUB_BRANCH}/"
        f"docs/articles/{filename}"
    )


def render_draft(title: str, filename: str, summary: str) -> str:
    article_url = article_github_url(filename)
    return f"""# Issue 标题（复制到 GitHub New Issue）

{title}

# Issue 正文（复制到描述框）

## 摘要

{summary}

## 延伸阅读

- 完整文章：[{title}]({article_url})
- SpeedCE 免费测速（中文）：{ZH_URL}
- 官网：{BASE_URL}

建议 Labels：`documentation`, `问答`
"""


def render_schedule_readme(entries: list[tuple[int, str, str]]) -> str:
    lines = [
        "# SpeedCE 知识库 · 100 天 Issue 发布日程",
        "",
        "> 每天发布 1 篇，手动复制到 GitHub Issues → New issue。",
        "> 建议标题用自然问句，可附 SpeedCE 地图截图。",
        "",
        "| Day | 草稿文件 | Issue 标题 |",
        "|-----|----------|------------|",
    ]
    for day, draft_file, title in entries:
        lines.append(f"| {day} | [{draft_file}]({draft_file}) | {title} |")
    lines.extend(
        [
            "",
            "## 发布步骤",
            "",
            "1. 查上表找到当天 `Day N` 对应文件",
            "2. GitHub → Issues → New issue",
            "3. 复制 **Issue 标题** 到 Title",
            "4. 复制 **Issue 正文** 以下到 Description（不含本说明标题行）",
            "5. 添加 Labels：`documentation`, `问答`",
            "",
            "## 重新生成",
            "",
            "```bash",
            "python3 scripts/generate_issue_drafts.py",
            "```",
            "",
        ]
    )
    return "\n".join(lines)


def main() -> None:
    DRAFTS_DIR.mkdir(parents=True, exist_ok=True)

    article_files = sorted(ARTICLES_DIR.glob("[0-9][0-9][0-9]-*.md"))
    if not article_files:
        raise SystemExit(f"No articles found in {ARTICLES_DIR}")

    schedule: list[tuple[int, str, str]] = []

    for article_path in article_files:
        raw = article_path.read_text(encoding="utf-8")
        meta, body_md = parse_frontmatter(raw)
        title = meta.get("title", article_path.stem)
        summary = strip_issue_body(body_md)

        draft_name = article_path.name
        draft_path = DRAFTS_DIR / draft_name
        draft_path.write_text(
            render_draft(title, article_path.name, summary),
            encoding="utf-8",
        )

        day = int(article_path.name[:3])
        schedule.append((day, draft_name, title))

    (DRAFTS_DIR / "README.md").write_text(
        render_schedule_readme(schedule),
        encoding="utf-8",
    )

    print(f"Generated {len(schedule)} issue drafts in {DRAFTS_DIR}")


if __name__ == "__main__":
    main()
