#!/bin/bash
# 重置数据库脚本 - 慎用！

set -e

echo "⚠️  警告：此操作将删除所有数据库数据！"
read -p "确定要重置数据库吗？(yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "操作已取消"
    exit 0
fi

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# 加载配置文件
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CONFIG_FILE="$PROJECT_ROOT/deploy_config.sh"

if [ ! -f "$CONFIG_FILE" ]; then
    echo -e "${RED}错误: 配置文件不存在: $CONFIG_FILE${NC}"
    exit 1
fi

source "$CONFIG_FILE"

# 构建 SSH 命令
SSH_CMD="ssh"
if [ -n "$SSH_KEY_PATH" ]; then
    SSH_CMD="ssh -i $SSH_KEY_PATH"
fi
SSH_TARGET="$SERVER_USER@$SERVER_HOST"

echo -e "${YELLOW}正在重置服务器数据库...${NC}"

$SSH_CMD "$SSH_TARGET" << ENDSSH
cd $DEPLOY_PATH

# 备份现有数据库
if [ -f homepage.db ]; then
    BACKUP_FILE="homepage.db.backup.\$(date +%Y%m%d_%H%M%S)"
    cp homepage.db "\$BACKUP_FILE"
    echo "✓ 已备份到: \$BACKUP_FILE"
fi

# 删除数据库
rm -f homepage.db

# 重新初始化
source venv/bin/activate
python scripts/init_db.py
python scripts/init_gomoku_db.py
python scripts/init_admin_db.py

# 重启服务
sudo systemctl restart homepage
echo "✓ 服务已重启"
ENDSSH

echo ""
echo -e "${GREEN}数据库重置完成！${NC}"
echo "默认管理员账户："
echo "  用户名: admin"
echo "  密码: admin123"
