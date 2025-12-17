# 数据库笔记

## SQL 基础

### 常用查询

```sql
-- 基本查询
SELECT * FROM users WHERE age > 18;

-- 连接查询
SELECT u.name, o.order_id
FROM users u
INNER JOIN orders o ON u.id = o.user_id;

-- 聚合函数
SELECT category, COUNT(*), AVG(price)
FROM products
GROUP BY category
HAVING COUNT(*) > 10;
```

### 索引优化

!!! tip "索引使用原则"
    - 为经常查询的列创建索引
    - 避免过多索引影响写入性能
    - 复合索引遵循最左前缀原则
    - 定期分析索引使用情况

```sql
-- 创建索引
CREATE INDEX idx_user_email ON users(email);

-- 复合索引
CREATE INDEX idx_user_name_age ON users(name, age);

-- 查看索引使用
EXPLAIN SELECT * FROM users WHERE email = 'test@example.com';
```

## SQLite

### 特点

- ✅ 轻量级、无需服务器
- ✅ 文件数据库，易于备份
- ✅ 适合中小型应用
- ⚠️ 并发写入受限

### Python 使用

```python
import sqlite3

# 连接数据库
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

# 插入数据
cursor.execute('INSERT INTO users (name, email) VALUES (?, ?)',
               ('张三', 'zhangsan@example.com'))

# 查询数据
cursor.execute('SELECT * FROM users')
users = cursor.fetchall()

conn.commit()
conn.close()
```

## PostgreSQL

### 高级特性

```sql
-- JSON 支持
CREATE TABLE products (
    id SERIAL PRIMARY KEY,
    data JSONB
);

INSERT INTO products (data) VALUES 
('{"name": "产品A", "price": 99.99}');

SELECT data->>'name' AS name FROM products;

-- 数组类型
CREATE TABLE tags (
    id SERIAL PRIMARY KEY,
    name TEXT,
    labels TEXT[]
);

INSERT INTO tags (name, labels) VALUES 
('文章1', ARRAY['Python', 'Web']);
```

### 性能调优

!!! example "配置优化"
    ```sql
    -- 查看慢查询
    SELECT query, calls, total_time, mean_time
    FROM pg_stat_statements
    ORDER BY total_time DESC
    LIMIT 10;
    
    -- 分析表统计
    ANALYZE users;
    
    -- 重建索引
    REINDEX TABLE users;
    ```

## Redis

### 数据类型

```python
import redis

r = redis.Redis(host='localhost', port=6379, db=0)

# 字符串
r.set('key', 'value')
r.get('key')

# 哈希
r.hset('user:1', 'name', '张三')
r.hgetall('user:1')

# 列表
r.lpush('queue', 'task1')
r.rpop('queue')

# 集合
r.sadd('tags', 'python', 'web')
r.smembers('tags')

# 有序集合
r.zadd('leaderboard', {'user1': 100, 'user2': 200})
r.zrange('leaderboard', 0, -1, withscores=True)
```

### 缓存策略

!!! tip "缓存模式"
    **Cache-Aside（旁路缓存）**
    ```python
    def get_user(user_id):
        # 先查缓存
        user = redis.get(f'user:{user_id}')
        if user:
            return json.loads(user)
        
        # 缓存未命中，查数据库
        user = db.query(User).get(user_id)
        
        # 写入缓存
        redis.setex(f'user:{user_id}', 3600, json.dumps(user))
        return user
    ```

## ORM - SQLAlchemy

### 模型定义

```python
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    email = Column(String(120), unique=True)
    
    # 关系
    posts = relationship('Post', back_populates='author')

class Post(Base):
    __tablename__ = 'posts'
    
    id = Column(Integer, primary_key=True)
    title = Column(String(200))
    user_id = Column(Integer, ForeignKey('users.id'))
    
    author = relationship('User', back_populates='posts')
```

### 查询技巧

```python
# 基本查询
users = session.query(User).filter(User.age > 18).all()

# 关联查询
posts = session.query(Post).join(User).filter(User.name == '张三').all()

# 聚合
from sqlalchemy import func
user_count = session.query(func.count(User.id)).scalar()

# 分页
page = session.query(User).offset(10).limit(10).all()
```

## 数据库设计原则

!!! warning "范式"
    - **第一范式（1NF）**: 列不可分
    - **第二范式（2NF）**: 消除部分依赖
    - **第三范式（3NF）**: 消除传递依赖

!!! tip "最佳实践"
    - 合理使用外键约束
    - 设计合适的索引
    - 避免NULL值（可能时）
    - 使用适当的数据类型
    - 定期备份数据
