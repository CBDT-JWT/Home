# 部署注意事项

## 🚨 重要提醒

部署脚本已配置为**不会覆盖**以下文件/目录：
- `homepage.db` - 数据库文件（包含所有用户数据、项目、留言等）
- `static/uploads/` - 用户上传的文件（缩略图、PDF、Markdown等）

## 📦 部署流程

### 常规部署（代码更新）
```bash
./deploy/deploy_quick.sh
```

这会：
1. 同步代码文件（不包括数据库和上传文件）
2. 检查数据库是否存在
3. 如果数据库存在，跳过初始化
4. 重启服务

### 首次部署或重置数据库
如果需要重新初始化数据库（⚠️ 会丢失所有数据）：

```bash
./scripts/reset_db.sh
```

这会：
1. 备份现有数据库到 `homepage.db.backup.YYYYMMDD_HHMMSS`
2. 删除现有数据库
3. 重新初始化所有表
4. 创建默认管理员账户

## 🔧 手动操作

### 仅初始化缺失的表

如果某些表缺失，可以单独运行初始化脚本：

```bash
# 在服务器上
cd ~/homepage
source venv/bin/activate
python scripts/init_admin_db.py    # 初始化管理员系统表
python scripts/init_gomoku_db.py   # 初始化五子棋表
python scripts/init_db.py          # 初始化基础表
```

### 查看数据库表

```bash
ssh www.weitao-jiang.cn "cd ~/homepage && source venv/bin/activate && python -c '
from app import app, db
app.app_context().push()
inspector = db.inspect(db.engine)
tables = inspector.get_table_names()
print(\"现有表:\", \", \".join(sorted(tables)))
'"
```

### 备份数据库

```bash
# 从服务器下载数据库备份
scp www.weitao-jiang.cn:~/homepage/homepage.db ./homepage.db.backup.$(date +%Y%m%d)
```

### 恢复数据库

```bash
# 上传数据库到服务器
scp ./homepage.db.backup.YYYYMMDD www.weitao-jiang.cn:~/homepage/homepage.db
ssh www.weitao-jiang.cn "sudo systemctl restart homepage"
```

## 📊 数据库表结构

当前系统包含以下表：

### 基础功能
- `visitor` - 访客记录
- `message` - 留言板

### 五子棋游戏
- `gomoku_room` - 游戏房间
- `gomoku_player` - 玩家信息
- `gomoku_move` - 走棋记录

### 管理员系统
- `admin` - 管理员账户
- `project` - 项目管理

## 🔐 默认管理员账户

每次初始化数据库后，会创建默认管理员：
- 用户名: `admin`
- 密码: `admin123`

**⚠️ 请在首次登录后立即修改密码！**

## 🛠️ 常见问题

### Q: 部署后项目数据丢失？
A: 检查是否是数据库被覆盖。从现在开始，部署脚本已排除数据库文件，不会再发生。

### Q: 上传的文件丢失？
A: 检查 `static/uploads/` 目录。部署脚本已排除该目录，不会被覆盖。

### Q: 某个表不存在？
A: 运行对应的初始化脚本（见上方"手动操作"部分）。

### Q: 如何完全重置？
A: 运行 `./scripts/reset_db.sh`，会备份并重置数据库。

## 📝 文件排除列表

以下文件/目录在部署时被排除（不会同步到服务器）：

```
.git/
.github/
venv/
__pycache__/
*.pyc
.env
.DS_Store
deploy/
deploy_*.sh
deploy_config.sh
homepage.db          ← 数据库文件
homepage.db-*        ← 数据库日志文件
static/uploads/      ← 用户上传文件
```

## 🎯 最佳实践

1. **定期备份数据库**（建议每周一次）
2. **修改默认管理员密码**
3. **测试环境先验证**再部署到生产环境
4. **查看部署日志**确认操作成功
5. **保存重要项目数据**的副本

---

最后更新: 2025-12-17
