---
title: 语法示例：一页写尽 Markdown
date: 2026-11-09 21:40
categories:
  - 说明
tags:
  - Markdown
  - 示例
  - 排版
summary: 把这套站点支持的 Markdown 语法集中放在一页里，当作写作时的速查表。
---

这一篇是**语法样张**，不是文章。它把站点当前支持的 Markdown 语法尽量都摆出来，写东西时可以回来对照。

## 段落与强调

普通段落直接写。行内可以是 *斜体*、**粗体**、***粗斜体***，也可以包住 `行内代码`。

需要删除线时用两个波浪线：~~这句话作废~~。

行内代码里可以放路径，例如 `content/pages/about.md` 或 `/static/uploads/night-walk.svg`。

## 链接

- 站内绝对路径：[关于页](/about/)
- 站内相对路径：[归档](../archive/) —— 注意这种写法在 Atom 里会失效，原因见下
- 外链：[Python](https://www.python.org/)
- 自动链接：<https://flask.palletsprojects.com/>
- 带标题的链接：[Markdown 指南](https://commonmark.org/help/ "CommonMark 帮助")

## 标题层级

### 三级标题

#### 四级标题

上面二、三级标题会自动生成锚点，鼠标悬停时出现一个 `#`。

## 列表

无序列表：

- 第一项
- 第二项
    - 嵌套一层
    - 再嵌套一层
- 第三项

有序列表：

1. 先写标题
2. 再写正文
3. 最后放进 `content/`

任务列表式的写法（用方括号表示状态，不会被渲染成复选框，纯文本）：

- [x] 已经完成的项
- [ ] 还没做的项

## 引用

> 单段引用，第一层。
>
> > 嵌套引用。
>
> 回到第一层。

带署名的引用常这样写：

> 有些句子适合留在夜里，等明天再读。
>
> —— 某篇旧文

## 代码

行内代码用反引号：`pip install -r requirements.txt`。

围栏代码块带语言标记时会高亮语法结构（本站不加载高亮库，仅做等宽排版）：

```python
def word_count(text: str) -> int:
    """中文按字计，拉丁文按词计。"""
    cjk = sum(1 for ch in text if "一" <= ch <= "鿿")
    latin = len(text.split())
    return cjk + latin
```

```javascript
// 指针视差：只写 translate，和 CSS 动画叠加而不打架
layer.el.style.translate = x + "px " + y + "px";
```

```bash
flask --app app.wsgi run -p 8000
```

```yaml
title: 标题
date: 2026-11-09 21:40
tags:
  - 示例
```

## 表格

| 语法 | 作用 | 备注 |
|------|------|------|
| `**粗体**` | 强调 | 双星号 |
| `*斜体*` | 强调 | 单星号 |
| `` `代码` `` | 行内代码 | 反引号 |
| `[文字](地址)` | 链接 | 方括号加圆括号 |
| `![说明](图片)` | 图片 | 前面多一个感叹号 |

右对齐与居中的列也可以指定：

| 左对齐 | 居中 | 右对齐 |
|:-------|:----:|-------:|
| A | B | 1 |
| 长一点的内容 | 中 | 22 |

## 定义列表

Markdown
: 一种用纯文本写结构化文档的标记语法。

Frontmatter
: 文件开头 `---` 之间的 YAML 元数据，站点从中读取标题、日期与标签。

## 脚注

这里有一个脚注引用[^1]，还有另一个[^note]。

[^1]: 脚注正文会渲染在文末，按引用顺序编号。

[^note]: 具名脚注也可以这样写。

## 提示块

!!! note "关于图片路径"
    写在 HTML 页面里用 `/static/uploads/xxx.png` 就行；但 Atom 订阅里会把这个路径补成绝对地址，用的是 `config.BASE_URL`。

!!! warning "上线前记得改 BASE_URL"
    它现在是 `http://localhost`。不改的话订阅器拿到的会是本机地址。

## 图片

站内图片用根路径。下面这张是随仓库附带的示例矢量图：

![夜路：雾与街灯的示意图](/static/uploads/night-walk.svg)

带标题的图片，鼠标悬停会显示 title：

![同一张图，更换了说明文字](/static/uploads/night-walk.svg "夜路示意图")

图片也可以加宽高属性（使用了 `attr_list` 扩展）：

![缩小显示](/static/uploads/night-walk.svg){ width="240" }

## 水平分割线

上面是一条分割线。

---

下面还有一条。

***

## HTML 混排

可以穿插 HTML，`md_in_html` 扩展保证块级元素内部的 Markdown 仍被解析：

<div class="markdown-demo">
  <p><strong>这是一个 HTML 块</strong>，里面的 <em>Markdown</em> 依然有效。</p>
</div>

也可以直接写行内标签：<kbd>Ctrl</kbd> + <kbd>C</kbd>，或者 <mark>高亮一小段</mark>。

## 常规标点替换

`smarty` 扩展会把直引号换成弯引号，并把 -- 换成长破折号：

他说 "这句话会被弯引号包住"，然后停了一下 -- 像是在等谁回答。

三个点会变成省略号：等等……

## 转义

需要显示原样字符时用反斜杠转义：\*不是斜体\*，\`不是代码\`。

## 收尾

以上是当前支持的语法集合。改 `content/` 里的文件后刷新页面即可看到效果，无需重启；独立页（如 `/about/`）走的是同一套渲染配置。
