# SpeedCE 站长知识库（speedce-docs）

> 多节点网站测速 · 网络排障 · 100 篇站长技术文章

**在线文档站：** https://freejbgo.github.io/speedce-docs/

| 入口 | 链接 |
|------|------|
| SpeedCE 官网 | https://www.speedce.com |
| 中文版测速 | https://speedce.com/?lang=zh-CN |
| 全部文章目录 | [docs/articles/README.md](docs/articles/README.md) |
| 按分类浏览 | [docs/categories.md](docs/categories.md) |

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

访问 http://localhost:4000/speedce-docs/

## 重新生成站点资源

```bash
python3 scripts/generate_site_assets.py   # sitemap、robots、分类页、文章导航
python3 scripts/generate_all_speedce_articles.py  # 重建全部 100 篇软文（可选）
```

## 开启 GitHub Pages

仓库 **Settings → Pages**：

- Source: **Deploy from a branch**
- Branch: **main** / **/docs**

保存后文档站发布至 `https://freejbgo.github.io/speedce-docs/`

## Topics 建议

`speedtest` `network-monitoring` `website-speed-test` `speedce` `devops` `web-performance`

---

SpeedCE — 覆盖中国各省市 · 全球节点 · 一键检测网络连通性  
联系：speedceads@gmail.com
