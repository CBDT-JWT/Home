#!/bin/bash
# 更新脚本 - 用于手动更新部署

set -e

DEPLOY_PATH="/home/$USER/homepage"

echo "开始更新应用..."

cd "$DEPLOY_PATH"

# 拉取最新代码
echo "拉取最新代码..."
git pull origin main

# 激活虚拟环境
source venv/bin/activate

# 更新依赖
echo "更新依赖..."
pip install -r requirements.txt

# 重启服务
echo "重启服务..."
sudo systemctl restart homepage

echo "更新完成！"
sudo systemctl status homepage --no-pager
