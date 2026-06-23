#!/usr/bin/env python3
"""Generate GitHub Issue drafts: Q&A, troubleshooting, and case studies."""

from pathlib import Path

from issue_posts_data import ISSUE_POSTS, REPO

REPO_ROOT = Path(__file__).resolve().parent.parent
ISSUES_DIR = REPO_ROOT / "docs" / "issue-drafts"


def render_issue(post: dict) -> str:
    related_lines = "\n".join(
        f"- [{name}]({REPO}/{name})" for name in post["related"]
    )
    return f"""# Issue 标题

{post["title"]}

---

# Issue 正文

{post["body"]}

---

## 延伸阅读

{related_lines}

---

**建议 Labels：** `{post["labels"]}`

> 本 Issue 为技术问答/排障讨论，非商业推广。欢迎在下方补充你的经验。
"""


def write_schedule() -> None:
    lines = [
        "# Issue 发布指南（48 篇）",
        "",
        "已整合原 100 篇素材，改写为**问答、案例、排障**风格，更适合在 Issues 里讨论。",
        "",
        "**发布节奏建议：** 每周 2～3 篇，不必每天发。",
        "",
        "| 序号 | 标题 | 草稿 |",
        "|------|------|------|",
    ]
    for post in ISSUE_POSTS:
        fn = f"{post['id']:03d}-{post['slug']}.md"
        lines.append(f"| {post['id']} | {post['title']} | [{fn}](./{fn}) |")

    lines.extend([
        "",
        "## 发布步骤",
        "",
        "1. GitHub → Issues → New issue",
        "2. 复制草稿中的 **Issue 标题** 到 Title",
        "3. 复制 **Issue 正文** 及以下到 Description",
        "4. 添加建议 Labels",
        "",
        "## 风格说明",
        "",
        "- 以「问 / 案例 / 排查步骤」为主，避免关键词堆砌",
        "- 完整长文见 `docs/articles/`，Issue 只做精选讨论",
        "- 重新生成：`python3 scripts/generate_issue_drafts.py`",
    ])
    (ISSUES_DIR / "README.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> None:
    ISSUES_DIR.mkdir(parents=True, exist_ok=True)

    # Remove old drafts (e.g. previous 100 files)
    for old in ISSUES_DIR.glob("*.md"):
        if old.name != "README.md":
            old.unlink()

    for post in ISSUE_POSTS:
        fn = f"{post['id']:03d}-{post['slug']}.md"
        (ISSUES_DIR / fn).write_text(render_issue(post), encoding="utf-8")

    write_schedule()
    print(f"Generated {len(ISSUE_POSTS)} issue drafts in {ISSUES_DIR}")


if __name__ == "__main__":
    main()
