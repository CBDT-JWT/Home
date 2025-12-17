# Web 开发笔记

## 前端技术

### HTML5 & CSS3

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>示例页面</title>
    <style>
        .container {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <div>内容1</div>
        <div>内容2</div>
    </div>
</body>
</html>
```

### CSS 技巧

!!! example "渐变背景"
    ```css
    .gradient-bg {
        background: linear-gradient(
            135deg,
            #667eea 0%,
            #764ba2 100%
        );
    }
    ```

## 后端框架

### Flask vs FastAPI

| 特性 | Flask | FastAPI |
|------|-------|---------|
| 速度 | 中等 | 极快 |
| 类型提示 | 可选 | 内置 |
| 异步支持 | 有限 | 原生支持 |
| 学习曲线 | 平缓 | 适中 |

## RESTful API 设计

### 最佳实践

```python
# 规范的 API 端点设计
GET    /api/users          # 获取用户列表
GET    /api/users/:id      # 获取单个用户
POST   /api/users          # 创建用户
PUT    /api/users/:id      # 更新用户
DELETE /api/users/:id      # 删除用户
```

### 错误处理

```python
from flask import jsonify

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'error': 'Not Found',
        'message': '请求的资源不存在'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'error': 'Internal Server Error',
        'message': '服务器内部错误'
    }), 500
```

## 部署

### Nginx 配置

```nginx
server {
    listen 80;
    server_name example.com;
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /static {
        alias /path/to/static;
        expires 30d;
    }
}
```

### Docker 部署

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "app:app"]
```

## 性能优化

!!! tip "优化建议"
    - 使用 CDN 加速静态资源
    - 启用 Gzip 压缩
    - 使用缓存（Redis/Memcached）
    - 数据库查询优化（索引、连接池）
    - 异步处理耗时任务
