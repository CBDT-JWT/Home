# 读书笔记

## 《Python编程：从入门到实践》

### 核心内容

本书适合Python初学者，分为两部分：

**第一部分：基础知识**

- 变量和数据类型
- 列表、字典、元组
- 条件语句和循环
- 函数和类

**第二部分：项目实战**

- 外星人入侵游戏
- 数据可视化
- Web应用

### 重点笔记

!!! quote "核心观点"
    学习编程最好的方式就是编写程序，从小项目开始，逐步提高。

```python
# 列表推导式
squares = [x**2 for x in range(1, 11)]

# 字典推导式
square_dict = {x: x**2 for x in range(1, 6)}
```

---

## 《深入理解计算机系统》

### 章节摘要

1. **计算机系统漫游** - 整体概览
2. **信息的表示和处理** - 数据编码
3. **程序的机器级表示** - 汇编语言
4. **处理器体系结构** - CPU设计
5. **优化程序性能** - 性能调优

### 关键概念

!!! info "重要概念"
    - **局部性原理**: 时间局部性和空间局部性
    - **抽象层次**: 从晶体管到高级语言
    - **缓存层次**: L1/L2/L3 缓存的作用

---

## 《设计模式：可复用面向对象软件的基础》

### 23种设计模式

#### 创建型模式

- 单例模式 (Singleton)
- 工厂方法 (Factory Method)
- 抽象工厂 (Abstract Factory)
- 建造者模式 (Builder)
- 原型模式 (Prototype)

#### 结构型模式

- 适配器模式 (Adapter)
- 桥接模式 (Bridge)
- 组合模式 (Composite)
- 装饰器模式 (Decorator)
- 外观模式 (Facade)
- 享元模式 (Flyweight)
- 代理模式 (Proxy)

#### 行为型模式

- 责任链模式 (Chain of Responsibility)
- 命令模式 (Command)
- 迭代器模式 (Iterator)
- 观察者模式 (Observer)
- 策略模式 (Strategy)
- 模板方法 (Template Method)
- 访问者模式 (Visitor)

### Python实现示例

```python
# 单例模式
class Singleton:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

# 工厂模式
class ShapeFactory:
    @staticmethod
    def create_shape(shape_type):
        if shape_type == "circle":
            return Circle()
        elif shape_type == "square":
            return Square()
```

---

## 《代码整洁之道》

### 核心原则

!!! quote "Robert C. Martin"
    "整洁的代码应当优雅且高效，逻辑应当直截了当，使人难以作弊；
    尽量减少依赖，使之便于维护。"

### 命名规则

- ✅ 使用有意义的名称
- ✅ 名称应该表达意图
- ✅ 避免使用误导性名称
- ✅ 做有意义的区分

```python
# ❌ 不好的命名
def get_them():
    list1 = []
    for x in the_list:
        if x[0] == 4:
            list1.append(x)
    return list1

# ✅ 好的命名
def get_flagged_cells():
    flagged_cells = []
    for cell in game_board:
        if cell.is_flagged():
            flagged_cells.append(cell)
    return flagged_cells
```

### 函数原则

!!! tip "函数应该"
    - 短小精悍
    - 只做一件事
    - 使用描述性名称
    - 参数越少越好（理想情况0-2个）
    - 没有副作用

---

## 阅读计划

- [ ] 《Effective Python》
- [ ] 《Flask Web开发实战》
- [ ] 《算法导论》
- [ ] 《数据密集型应用系统设计》
