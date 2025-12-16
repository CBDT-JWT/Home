#!/bin/bash
# 服务器初始化脚本
# 在 Ubuntu 服务器上运行此脚本来设置环境

set -e

echo "========================================="
echo "个人主页项目 - 服务器部署脚本"
echo "========================================="

# 颜色输出
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 配置变量（根据实际情况修改）
DEPLOY_USER="$USER"
DEPLOY_PATH="/home/$DEPLOY_USER/homepage"
APP_PORT=5000
DOMAIN_NAME="your-domain.com"  # 可选：如果有域名

echo -e "${YELLOW}步骤 1/7: 更新系统包...${NC}"
sudo apt update
sudo apt upgrade -y

echo -e "${YELLOW}步骤 2/7: 安装必要软件...${NC}"
sudo apt install -y python3.11 python3.11-venv python3-pip git nginx supervisor

echo -e "${YELLOW}步骤 3/7: 创建部署目录...${NC}"
if [ ! -d "$DEPLOY_PATH" ]; then
    mkdir -p "$DEPLOY_PATH"
    echo -e "${GREEN}创建目录: $DEPLOY_PATH${NC}"
fi

echo -e "${YELLOW}步骤 4/7: 克隆代码仓库...${NC}"
echo "请输入你的 GitHub 仓库 URL (例如: https://github.com/username/homepage.git):"
read REPO_URL

if [ ! -d "$DEPLOY_PATH/.git" ]; then
    git clone "$REPO_URL" "$DEPLOY_PATH"
else
    cd "$DEPLOY_PATH"
    git pull origin main
fi

cd "$DEPLOY_PATH"

echo -e "${YELLOW}步骤 5/7: 设置 Python 虚拟环境...${NC}"
if [ ! -d "venv" ]; then
    python3.11 -m venv venv
fi
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

echo -e "${YELLOW}步骤 6/7: 配置 Systemd 服务...${NC}"
sudo tee /etc/systemd/system/homepage.service > /dev/null <<EOF
[Unit]
Description=Personal Homepage Flask Application
After=network.target

[Service]
User=$DEPLOY_USER
WorkingDirectory=$DEPLOY_PATH
Environment="PATH=$DEPLOY_PATH/venv/bin"
Environment="PORT=$APP_PORT"
ExecStart=$DEPLOY_PATH/venv/bin/gunicorn -w 4 -b 127.0.0.1:$APP_PORT app:app
Restart=always

[Install]
WantedBy=multi-user.target
EOF

echo -e "${YELLOW}步骤 7/7: 配置 Nginx 反向代理...${NC}"
sudo tee /etc/nginx/sites-available/homepage > /dev/null <<EOF
server {
    listen 80;
    server_name $DOMAIN_NAME;

    location / {
        proxy_pass http://127.0.0.1:$APP_PORT;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # 静态文件缓存
    location /static {
        alias $DEPLOY_PATH/static;
        expires 30d;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# 启用 Nginx 站点
sudo ln -sf /etc/nginx/sites-available/homepage /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# 测试 Nginx 配置
sudo nginx -t

# 启动服务
echo -e "${GREEN}启动服务...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable homepage
sudo systemctl start homepage
sudo systemctl restart nginx

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}部署完成！${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo "服务状态检查："
sudo systemctl status homepage --no-pager
echo ""
echo "访问地址："
echo "  - 本地: http://localhost"
if [ "$DOMAIN_NAME" != "your-domain.com" ]; then
    echo "  - 域名: http://$DOMAIN_NAME"
fi
echo ""
echo "常用命令："
echo "  - 查看日志: sudo journalctl -u homepage -f"
echo "  - 重启服务: sudo systemctl restart homepage"
echo "  - 停止服务: sudo systemctl stop homepage"
echo "  - 查看状态: sudo systemctl status homepage"
echo ""
