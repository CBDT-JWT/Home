# 课程笔记

## CS50: 计算机科学导论

### 课程信息

- **学校**: 哈佛大学
- **平台**: edX
- **讲师**: David J. Malan
- **难度**: 入门

### Week 1-2: C语言基础

```c
#include <stdio.h>

int main(void)
{
    printf("Hello, World!\n");
    return 0;
}
```

### Week 3-4: 算法

!!! example "排序算法对比"
    | 算法 | 最好 | 平均 | 最坏 | 空间 |
    |------|------|------|------|------|
    | 冒泡 | O(n) | O(n²) | O(n²) | O(1) |
    | 选择 | O(n²) | O(n²) | O(n²) | O(1) |
    | 插入 | O(n) | O(n²) | O(n²) | O(1) |
    | 归并 | O(n log n) | O(n log n) | O(n log n) | O(n) |
    | 快排 | O(n log n) | O(n log n) | O(n²) | O(log n) |

### Week 5-6: 数据结构

```c
// 链表节点
typedef struct node
{
    int number;
    struct node *next;
}
node;

// 哈希表
typedef struct
{
    node *buckets[HASH_SIZE];
}
hashtable;
```

---

## Machine Learning - Andrew Ng

### 课程概览

Coursera上最受欢迎的机器学习课程。

### 监督学习

#### 线性回归

$$ h_\theta(x) = \theta_0 + \theta_1 x $$

成本函数:

$$ J(\theta) = \frac{1}{2m} \sum_{i=1}^{m} (h_\theta(x^{(i)}) - y^{(i)})^2 $$

梯度下降:

$$ \theta_j := \theta_j - \alpha \frac{\partial}{\partial \theta_j} J(\theta) $$

```python
import numpy as np

def gradient_descent(X, y, theta, alpha, iterations):
    m = len(y)
    
    for _ in range(iterations):
        predictions = X.dot(theta)
        errors = predictions - y
        gradient = (1/m) * X.T.dot(errors)
        theta = theta - alpha * gradient
    
    return theta
```

#### 逻辑回归

Sigmoid函数:

$$ g(z) = \frac{1}{1 + e^{-z}} $$

```python
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

def logistic_regression(X, y, theta, alpha, iterations):
    m = len(y)
    
    for _ in range(iterations):
        h = sigmoid(X.dot(theta))
        gradient = (1/m) * X.T.dot(h - y)
        theta = theta - alpha * gradient
    
    return theta
```

### 神经网络

!!! info "关键概念"
    - 前向传播 (Forward Propagation)
    - 反向传播 (Back Propagation)
    - 激活函数 (Activation Functions)
    - 损失函数 (Loss Functions)

---

## Full Stack Web Development

### 前端技术栈

- **HTML5/CSS3**: 结构和样式
- **JavaScript/TypeScript**: 交互逻辑
- **React/Vue**: 前端框架
- **状态管理**: Redux/Vuex

### 后端技术栈

- **Node.js/Express**: JavaScript后端
- **Python/Django/Flask**: Python后端
- **数据库**: MySQL/PostgreSQL/MongoDB
- **缓存**: Redis/Memcached

### 项目实战

```javascript
// Express.js 基础路由
const express = require('express');
const app = express();

app.get('/api/users', (req, res) => {
    res.json({ users: ['Alice', 'Bob'] });
});

app.post('/api/users', (req, res) => {
    const { name } = req.body;
    // 保存用户逻辑
    res.status(201).json({ message: 'User created' });
});

app.listen(3000, () => {
    console.log('Server running on port 3000');
});
```

---

## 数据结构与算法

### 常用数据结构

```python
# 栈 (Stack)
class Stack:
    def __init__(self):
        self.items = []
    
    def push(self, item):
        self.items.append(item)
    
    def pop(self):
        return self.items.pop()

# 队列 (Queue)
from collections import deque

class Queue:
    def __init__(self):
        self.items = deque()
    
    def enqueue(self, item):
        self.items.append(item)
    
    def dequeue(self):
        return self.items.popleft()

# 二叉搜索树 (BST)
class TreeNode:
    def __init__(self, val):
        self.val = val
        self.left = None
        self.right = None

def insert_bst(root, val):
    if not root:
        return TreeNode(val)
    
    if val < root.val:
        root.left = insert_bst(root.left, val)
    else:
        root.right = insert_bst(root.right, val)
    
    return root
```

### 经典算法

!!! example "动态规划 - 斐波那契数列"
    ```python
    def fib_dp(n):
        if n <= 1:
            return n
        
        dp = [0] * (n + 1)
        dp[1] = 1
        
        for i in range(2, n + 1):
            dp[i] = dp[i-1] + dp[i-2]
        
        return dp[n]
    ```

---

## 学习资源

### 在线平台

- [Coursera](https://www.coursera.org/)
- [edX](https://www.edx.org/)
- [Udacity](https://www.udacity.com/)
- [MIT OpenCourseWare](https://ocw.mit.edu/)

### 练习平台

- [LeetCode](https://leetcode.com/)
- [HackerRank](https://www.hackerrank.com/)
- [CodeWars](https://www.codewars.com/)
