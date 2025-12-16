# 个人主页

一个简洁的个人主页项目，采用 Python Flask 后端 + HTML/CSS 前端构建。

## 功能特性

- ✨ 简洁优雅的首页设计
- 🎨 渐变色背景（可替换为自定义图片）
- 🔄 GitHub Actions CI/CD 自动化部署
- 🚀 Flask 后端服务

## 项目结构

```
homepage/
├── app.py                    # Flask 应用主文件
├── requirements.txt          # Python 依赖
├── .gitignore               # Git 忽略文件
├── static/                  # 静态文件目录
│   ├── index.html          # 首页
│   └── images/             # 图片目录（放置背景图）
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions 配置
└── README.md               # 项目说明
```

## 快速开始

### 1. 克隆项目

```bash
git clone <your-repo-url>
cd homepage
```

### 2. 安装依赖

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. 运行应用

```bash
python app.py
```

访问 http://localhost:5000 查看效果。

### 4. 自定义背景图片（可选）

如果你想使用自己的背景图片：

1. 将你的背景图片放到 `static/images/` 目录下，例如 `background.jpg`
2. 编辑 `static/index.html`，找到 CSS 中的注释部分：
   ```css
   /* 如果你想使用图片作为背景，请取消下面的注释并注释掉上面的 background 属性 */
   /*
   .background {
       background-image: url('/images/background.jpg');
   }
   */
   ```
3. 取消注释并修改图片路径为你的图片名称
4. 注释掉原来的渐变背景样式

## 生产环境部署

### 使用 Gunicorn 运行

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

参数说明：
- `-w 4`: 使用 4 个 worker 进程
- `-b 0.0.0.0:8000`: 绑定到所有网络接口的 8000 端口

### 环境变量

- `PORT`: 指定运行端口（默认：5000）

```bash
export PORT=8000
python app.py
```

## GitHub Actions CI/CD

项目已配置 GitHub Actions 自动化流程，每次推送到 main/master 分支时会自动：

1. ✅ 运行代码检查（flake8）
2. ✅ 运行测试（pytest）
3. ✅ 构建项目

CI/CD 配置文件位于 `.github/workflows/ci-cd.yml`。

### 启用 CI/CD

1. 将代码推送到 GitHub
2. GitHub Actions 会自动运行
3. 在仓库的 "Actions" 标签页查看运行状态

### 配置部署（可选）

如需自动部署到服务器，可以在 `.github/workflows/ci-cd.yml` 中取消注释 `deploy` job，并配置：

- SSH 密钥
- 服务器地址
- 部署脚本

## 技术栈

- **后端**: Python 3.11+ / Flask 3.0
- **前端**: HTML5 / CSS3
- **部署**: Gunicorn
- **CI/CD**: GitHub Actions

## 开发建议

- 使用虚拟环境管理 Python 依赖
- 推送代码前确保通过本地测试
- 定期更新依赖包

## API 接口

- `GET /`: 返回首页
- `GET /health`: 健康检查接口

## 许可证

MIT License

## 作者

[Your Name]

## 贡献

欢迎提交 Issue 和 Pull Request！
