# SpeedCE 站长知识库（SpeedCE-Docs）

> 多节点网站测速 · 网络排障 · 100 篇站长技术文章

**在线文档站：** https://freejbgo.github.io/SpeedCE-Docs/

| 入口 | 链接 |
|------|------|
| SpeedCE 官网 | https://www.speedce.com |
| 中文版测速 | https://speedce.com/?lang=zh-CN |
| 全部文章目录 | [docs/articles/README.md](docs/articles/README.md) |
| 按分类浏览 | [docs/categories.md](docs/categories.md) |
| GitHub 仓库 | https://github.com/freejbgo/SpeedCE-Docs |

## 仓库内容

- **100 篇技术文章** — `docs/articles/`（基础知识、产品专题、场景实战、SEO 长尾、云架构、行业应用等）
- **GitHub Pages 文档站** — `docs/` 目录，Jekyll 自动构建
- **生成脚本** — `scripts/` 软文生成与站点资源生成

## 本地预览文档站

```bash
cd docs
bundle install
bundle exec jekyll serve
```

访问 http://localhost:4000/SpeedCE-Docs/

## 重新生成站点资源

```bash
python3 scripts/generate_site_assets.py   # sitemap、robots、分类页、文章导航
python3 scripts/generate_all_speedce_articles.py  # 重建全部 100 篇软文（可选）
```

## 开启 GitHub Pages

仓库 **Settings → Pages**：

- Source: **Deploy from a branch**
- Branch: **main** / **/docs**

保存后文档站发布至 `https://freejbgo.github.io/SpeedCE-Docs/`

> **注意：** 若仓库为 **Private**，免费账号无法对外发布 Pages；需改为 **Public**，或升级 GitHub Pro 才能从私有仓库发布公开 Pages。要做 SEO 收录，建议将仓库设为 **Public**。

## Topics 建议

`speedtest` `network-monitoring` `website-speed-test` `speedce` `devops` `web-performance`

---

SpeedCE — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性  
联系：speedceads@gmail.com
