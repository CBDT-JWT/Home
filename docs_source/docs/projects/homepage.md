# 个人主页项目

## 项目概述

一个现代化的个人主页，集成了Flask后端、数据库和笔记系统。

- **在线地址**: https://www.weitao-jiang.cn
- **GitHub**: https://github.com/CBDT-JWT/Home

## 技术架构

### 后端

```
Flask 3.0 + SQLAlchemy 3.1
├── app.py              # 主应用
├── 数据模型
│   ├── Visitor         # 访客统计
│   └── Message         # 留言板
└── API接口
    ├── /health         # 健康检查
    ├── /api/visitors   # 访客统计
    └── /api/messages   # 留言板
```

### 前端

- HTML5 / CSS3
- 渐变背景设计
- 响应式布局

### 数据库

- SQLite（轻量级）
- 访客记录表
- 留言表

### 部署

```
服务器: Ubuntu 24.04 (阿里云ECS)
Web服务器: Nginx
应用服务器: Gunicorn
进程管理: systemd
SSL证书: 自签名（测试）
```

## 项目结构

```
homepage/
├── app.py                    # Flask应用
├── requirements.txt          # 依赖
├── deploy_config.sh         # 部署配置
│
├── static/                  # 静态文件
│   ├── index.html
│   └── notes/              # MkDocs构建输出
│
├── scripts/                 # 工具脚本
│   ├── init_db.py
│   └── manage_db.py
│
├── deploy/                  # 部署脚本
│   ├── deploy_local.sh
│   └── deploy_quick.sh
│
└── docs_source/            # 笔记源文件
    ├── mkdocs.yml
    └── docs/
```

## 核心功能

### 1. 访客统计

自动记录每次访问：

```python
@app.route('/')
def index():
    visitor = Visitor(
        ip_address=request.remote_addr,
        user_agent=request.headers.get('User-Agent'),
        page='/'
    )
    db.session.add(visitor)
    db.session.commit()
    return send_from_directory('static', 'index.html')
```

### 2. 留言板API

```python
@app.route('/api/messages', methods=['GET', 'POST'])
def messages():
    if request.method == 'POST':
        data = request.get_json()
        message = Message(
            name=data.get('name'),
            email=data.get('email'),
            content=data.get('content')
        )
        db.session.add(message)
        db.session.commit()
        return jsonify(message.to_dict()), 201
    else:
        messages = Message.query.order_by(
            Message.created_at.desc()
        ).all()
        return jsonify([m.to_dict() for m in messages])
```

### 3. 笔记系统

使用MkDocs构建静态文档站点，集成到 `/notes` 路径。

## 部署流程

### 快速部署

```bash
# 1. 配置服务器信息
cp deploy/deploy_config.example.sh deploy_config.sh
vim deploy_config.sh

# 2. 执行部署
./deploy/deploy_quick.sh
```

### systemd服务

```ini
[Unit]
Description=Homepage Flask Application
After=network.target

[Service]
Type=notify
User=root
WorkingDirectory=/root/homepage
Environment="PATH=/root/homepage/venv/bin"
ExecStart=/root/homepage/venv/bin/gunicorn \
    -w 4 \
    -b 127.0.0.1:5000 \
    app:app

[Install]
WantedBy=multi-user.target
```

### Nginx配置

```nginx
server {
    listen 443 ssl http2;
    server_name www.weitao-jiang.cn;
    
    ssl_certificate /etc/nginx/ssl/homepage.crt;
    ssl_certificate_key /etc/nginx/ssl/homepage.key;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /notes {
        alias /root/homepage/static/notes;
        index index.html;
    }
    
    location /static {
        alias /root/homepage/static;
        expires 30d;
    }
}
```

## 开发笔记

### 遇到的问题

#### 1. 服务器无法访问外网

**问题**: Let's Encrypt证书申请失败

**解决**: 使用自签名证书或阿里云免费SSL证书

#### 2. GitHub Actions连接超时

**问题**: 服务器私网IP导致无法连接

**解决**: 使用本地部署脚本代替

#### 3. 数据库路径问题

**问题**: 脚本移动到 `scripts/` 后导入失败

**解决**: 添加路径到 sys.path

```python
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```

## 后续计划

- [ ] 添加留言板前端界面
- [ ] 集成真实SSL证书
- [ ] 添加访客统计可视化
- [ ] 博客系统集成
- [ ] 评论功能
- [ ] 搜索功能
- [ ] 标签系统

## 参考资源

- [Flask官方文档](https://flask.palletsprojects.com/)
- [SQLAlchemy文档](https://docs.sqlalchemy.org/)
- [MkDocs文档](https://www.mkdocs.org/)
- [Material for MkDocs](https://squidfunk.github.io/mkdocs-material/)
