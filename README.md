# borelo

个人博客：Flask + Jinja2 动态渲染 Markdown，SQLite 记录阅读与点赞，Docker Compose 仅运行 nginx 反代。

## 要求

- Python 3.10+
- Docker / Docker Compose（可选，用于 nginx）

## 快速开始

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# 开发可直接：
flask --app app.wsgi run -p 8000

# 或生产式：
gunicorn -b 127.0.0.1:8000 app.wsgi:app
```

浏览器打开 <http://127.0.0.1:8000>。

若要用 nginx 反代到 80 端口：

```bash
# 先在本机启动 gunicorn（如上）
docker compose up -d
```

访问 <http://localhost/>。nginx 将请求转到宿主机 `8000` 端口。

## 写文章

在 `content/` 下新增 `.md` 文件，文件名（不含扩展名）即文章 slug。示例 frontmatter：

```yaml
---
title: 标题
date: 2026-11-09
categories:
  - 随笔
tags:
  - 示例
summary: 可选摘要
---
```

修改或新增后刷新页面即可，无需重建静态站。

## 站点配置

编辑根目录 `config.py`：站点名、作者、简介、上线日期、`BASE_URL`（Atom 里的绝对链接）等。

## 数据

- 文章：仅 `content/*.md`
- 观看 / 点赞：`data/blog.sqlite`（启动时自动创建，已 gitignore）
- 备份：复制 `data/blog.sqlite`
- 重置计数：删除该文件后重启应用

## 主要路由

| 路径 | 说明 |
|------|------|
| `/` | 首页 |
| `/post/<slug>/` | 文章 |
| `/archive/` | 归档 |
| `/categories/`、`/category/<name>/` | 分类 |
| `/tags/`、`/tag/<name>/` | 标签 |
| `/feed.atom` | Atom 订阅 |
| `/api/view/<slug>`、`/api/like/<slug>` | 观看 / 点赞 |

浅色 / 深色模式由页眉按钮切换，偏好保存在浏览器 `localStorage`。
