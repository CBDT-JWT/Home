# 项目结构说明

```
homepage/
│
├── 📄 核心文件
│   ├── app.py                      # Flask 应用主文件
│   ├── requirements.txt            # Python 依赖列表
│   ├── .gitignore                  # Git 忽略文件
│   ├── README.md                   # 项目说明文档
│   └── deploy_config.sh            # 部署配置（不提交到 Git）
│
├── 📁 static/                      # 静态资源目录
│   ├── index.html                  # 首页 HTML
│   └── images/                     # 图片资源目录
│
├── 📁 scripts/                     # 工具脚本目录
│   ├── init_db.py                  # 数据库初始化脚本
│   └── manage_db.py                # 数据库管理工具
│
├── 📁 deploy/                      # 部署相关目录
│   ├── deploy_local.sh             # 从 GitHub 拉取并部署
│   ├── deploy_quick.sh             # 快速部署当前代码
│   ├── deploy_config.example.sh   # 配置文件模板
│   ├── setup_server.sh             # 服务器初始化脚本
│   ├── update.sh                   # 更新脚本
│   │
│   └── 📝 文档
│       ├── README.md               # 部署说明
│       ├── DEPLOYMENT.md           # 详细部署文档
│       ├── DEPLOY_CONFIG.md        # 配置说明
│       ├── LOCAL_DEPLOY.md         # 本地部署指南
│       ├── SECRETS_CONFIG.md       # 密钥配置说明
│       └── UPDATE_NOTES.md         # 更新日志
│
└── 📁 .github/                     # GitHub 配置
    └── workflows/
        └── ci-cd.yml               # GitHub Actions 配置

```

## 📂 目录说明

### 根目录文件

| 文件 | 说明 |
|------|------|
| `app.py` | Flask 应用主文件，包含所有路由和数据库模型 |
| `requirements.txt` | Python 依赖包列表 |
| `README.md` | 项目主文档，包含快速开始指南 |
| `.gitignore` | Git 忽略配置，排除数据库文件、虚拟环境等 |
| `deploy_config.sh` | 部署配置文件（包含服务器信息，不提交到 Git） |
| `homepage.db` | SQLite 数据库文件（不提交到 Git） |

### static/ - 静态资源

存放前端静态文件：
- `index.html` - 主页 HTML
- `images/` - 图片资源（背景图、logo 等）

### scripts/ - 工具脚本

数据库相关工具：
- `init_db.py` - 初始化数据库表和示例数据
- `manage_db.py` - 数据库管理（查看统计、清理数据、导出备份）

**使用方法：**
```bash
# 初始化数据库
python scripts/init_db.py

# 查看统计
python scripts/manage_db.py stats

# 清理旧数据
python scripts/manage_db.py clear 30

# 导出数据
python scripts/manage_db.py export
```

### deploy/ - 部署相关

所有部署相关的脚本和文档：

**部署脚本：**
- `deploy_local.sh` - 从 GitHub 克隆最新代码并部署
- `deploy_quick.sh` - 直接部署当前目录到服务器
- `deploy_config.example.sh` - 配置文件模板
- `setup_server.sh` - 服务器环境初始化
- `update.sh` - 快速更新脚本

**文档：**
- `README.md` - 部署快速指南
- `DEPLOYMENT.md` - 详细部署步骤
- `DEPLOY_CONFIG.md` - 配置文件说明
- `LOCAL_DEPLOY.md` - 本地部署指南
- `SECRETS_CONFIG.md` - 密钥和环境变量配置
- `UPDATE_NOTES.md` - 部署更新记录

**配置方法：**
```bash
# 1. 复制配置模板
cp deploy/deploy_config.example.sh deploy_config.sh

# 2. 编辑配置文件
vim deploy_config.sh

# 3. 执行部署
./deploy/deploy_quick.sh
```

### .github/ - CI/CD

GitHub Actions 自动化配置：
- `workflows/ci-cd.yml` - 自动化部署流程

## 🔧 开发工作流

### 本地开发

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 初始化数据库
python scripts/init_db.py

# 3. 运行应用
python app.py
```

### 部署到服务器

```bash
# 1. 配置部署信息
cp deploy/deploy_config.example.sh deploy_config.sh
vim deploy_config.sh

# 2. 执行部署
./deploy/deploy_quick.sh
```

### 数据库管理

```bash
# 查看统计
python scripts/manage_db.py stats

# 清理数据
python scripts/manage_db.py clear 30

# 导出备份
python scripts/manage_db.py export
```

## 📝 文件关系图

```
开发流程:
  编辑代码 → git commit → git push
                              ↓
                      GitHub Repository
                              ↓
                    deploy/deploy_local.sh
                              ↓
                         生产服务器

数据库:
  app.py → 定义模型
     ↓
  scripts/init_db.py → 创建表
     ↓
  homepage.db → 存储数据
     ↓
  scripts/manage_db.py → 管理维护

部署:
  deploy_config.sh → 配置信息
     ↓
  deploy/*.sh → 执行部署
     ↓
  服务器 → 运行应用
```

## 🎯 最佳实践

1. **不要提交敏感信息**
   - `deploy_config.sh` 已在 `.gitignore` 中
   - `homepage.db` 数据库文件也已排除

2. **部署前测试**
   - 本地运行 `python app.py` 确认无错
   - 检查数据库是否正常

3. **定期备份**
   - 使用 `python scripts/manage_db.py export` 导出数据
   - 备份服务器上的 `homepage.db`

4. **文档更新**
   - 修改功能后更新 README.md
   - 部署变更记录在 deploy/UPDATE_NOTES.md
