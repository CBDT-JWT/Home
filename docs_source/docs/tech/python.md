# Python 学习笔记

## 基础知识

### 数据类型

Python 的基本数据类型包括：

```python
# 数字
integer = 42
floating = 3.14
complex_num = 1 + 2j

# 字符串
text = "Hello, Python!"

# 列表
my_list = [1, 2, 3, 4, 5]

# 字典
my_dict = {"name": "Python", "version": 3.11}

# 集合
my_set = {1, 2, 3, 4, 5}

# 元组
my_tuple = (1, 2, 3)
```

### 函数定义

```python
def greet(name: str) -> str:
    """问候函数"""
    return f"Hello, {name}!"

# 使用类型提示
def add_numbers(a: int, b: int) -> int:
    return a + b
```

## Web 开发 - Flask

### 基础应用

```python
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, Flask!"

@app.route('/api/data')
def get_data():
    return jsonify({"message": "Success"})

if __name__ == '__main__':
    app.run(debug=True)
```

### 数据库集成

```python
from flask_sqlalchemy import SQLAlchemy

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    email = db.Column(db.String(120), unique=True)
```

## 常用库

### 数据处理

!!! example "Pandas 数据处理"
    ```python
    import pandas as pd
    
    # 读取 CSV
    df = pd.read_csv('data.csv')
    
    # 数据清洗
    df.dropna(inplace=True)
    
    # 数据分组
    grouped = df.groupby('category').sum()
    ```

### 异步编程

```python
import asyncio

async def fetch_data(url):
    # 模拟异步请求
    await asyncio.sleep(1)
    return f"Data from {url}"

async def main():
    tasks = [fetch_data(f"url_{i}") for i in range(5)]
    results = await asyncio.gather(*tasks)
    print(results)

# 运行
asyncio.run(main())
```

## 最佳实践

!!! tip "代码规范"
    - 遵循 PEP 8 代码风格
    - 使用类型提示提高代码可读性
    - 编写文档字符串
    - 使用虚拟环境管理依赖

!!! warning "注意事项"
    - 避免使用可变对象作为默认参数
    - 注意 GIL（全局解释器锁）对多线程的影响
    - 正确处理异常

## 参考资源

- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [Real Python](https://realpython.com/)
- [Python Cookbook](https://python3-cookbook.readthedocs.io/)
