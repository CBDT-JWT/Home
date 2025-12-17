# MkDocs 笔记系统

本目录包含使用 MkDocs 构建的个人笔记系统。

## 📁 目录结构

```
docs_source/
├── mkdocs.yml          # MkDocs配置文件
├── docs/               # Markdown文档源文件
│   ├── index.md        # 首页
│   ├── tech/           # 技术笔记
│   ├── study/          # 学习笔记
│   ├── projects/       # 项目文档
│   └── about.md        # 关于页面
└── README.md           # 本文件
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install mkdocs-material
```

### 2. 本地预览

```bash
cd docs_source
mkdocs serve
```

访问 http://localhost:8000 预览笔记站点。

### 3. 构建文档

```bash
# 使用构建脚本
./scripts/build_docs.sh

# 或手动构建
cd docs_source
mkdocs build
```

构建后的静态文件会输出到 `static/notes/` 目录。

## ✍️ 添加新笔记

### 1. 创建 Markdown 文件

在 `docs/` 目录下创建新的 `.md` 文件：

```bash
# 例如添加一个 JavaScript 笔记
touch docs/tech/javascript.md
```

### 2. 更新导航

编辑 `mkdocs.yml` 的 `nav` 部分：

```yaml
nav:
  - 技术笔记:
      - Python: tech/python.md
      - JavaScript: tech/javascript.md  # 新增
```

### 3. 重新构建

```bash
./scripts/build_docs.sh
```

## 📝 Markdown 语法

MkDocs Material 支持丰富的 Markdown 扩展：

### 代码块

\`\`\`python
def hello():
    print("Hello, World!")
\`\`\`

### 提示框

\`\`\`
!!! tip "提示"
    这是一个提示框

!!! warning "警告"
    这是一个警告框

!!! example "示例"
    这是一个示例框
\`\`\`

### 数学公式

行内公式: `$E = mc^2$`

块级公式:
\`\`\`
$$ 
\sum_{i=1}^{n} i = \frac{n(n+1)}{2}
$$
\`\`\`

### 表格

```markdown
| 列1 | 列2 | 列3 |
|-----|-----|-----|
| A   | B   | C   |
```

### 任务列表

```markdown
- [x] 完成的任务
- [ ] 未完成的任务
```

## 🎨 主题配置

当前使用 Material for MkDocs 主题，支持：

- ✨ 深色/浅色模式切换
- 🔍 全文搜索
- 📱 响应式设计
- 🎯 代码高亮
- 📋 代码复制
- 🏷️ 标签系统

修改主题配置请编辑 `mkdocs.yml` 的 `theme` 部分。

## 🌐 部署

### 自动部署

部署脚本会自动构建文档：

```bash
./deploy/deploy_quick.sh
```

### 手动部署

1. 构建文档：
```bash
cd docs_source
mkdocs build
```

2. 确保 `static/notes/` 被同步到服务器

3. 服务器上 Nginx 配置：
```nginx
location /notes {
    alias /root/homepage/static/notes;
    index index.html;
}
```

## 📚 文档分类

### tech/ - 技术笔记
编程语言、框架、工具的学习笔记

- `python.md` - Python 相关
- `web.md` - Web 开发
- `database.md` - 数据库

### study/ - 学习笔记
读书笔记和课程学习记录

- `books.md` - 读书笔记
- `courses.md` - 课程笔记

### projects/ - 项目文档
个人项目的技术文档

- `homepage.md` - 本项目文档

## 🔗 相关链接

- [MkDocs 官方文档](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
- [Markdown 语法](https://markdown.com.cn/)

## 💡 最佳实践

1. **文件命名**: 使用小写字母和连字符，如 `my-note.md`
2. **目录组织**: 按主题分类，保持层级简单
3. **图片管理**: 图片放在 `docs/images/` 目录
4. **定期构建**: 每次修改后重新构建确保更新
5. **版本控制**: Markdown 源文件提交到 Git，构建产物不提交

## 🛠️ 常用命令

```bash
# 本地预览
cd docs_source && mkdocs serve

# 构建文档
./scripts/build_docs.sh

# 新建笔记
touch docs/tech/new-topic.md

# 查看配置
cat mkdocs.yml
```
