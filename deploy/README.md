# 使用 SSH Deploy Action 部署指南

本项目使用 [easingthemes/ssh-deploy](https://github.com/easingthemes/ssh-deploy) 实现自动化部署。

## 🎯 部署流程

```
本地推送 → GitHub Actions → SSH 部署 → 服务器更新 → 自动重启
```

---

## � 快速开始

### 步骤 1：服务器初始化

在服务器上运行：

```bash
chmod +x deploy/setup.sh
./deploy/setup.sh
```

### 步骤 2：生成 SSH 密钥

```bash
ssh-keygen -t ed25519 -f ~/.ssh/github_deploy -N ''
cat ~/.ssh/github_deploy.pub >> ~/.ssh/authorized_keys
cat ~/.ssh/github_deploy  # 复制私钥到 GitHub Secrets
```

### 步骤 3：配置 GitHub Secrets

在 GitHub 仓库中配置以下 Secrets：

| Secret 名称 | 说明 | 示例 |
|------------|------|------|
| `SSH_PRIVATE_KEY` | SSH 私钥 | `-----BEGIN OPENSSH PRIVATE KEY-----...` |
| `REMOTE_HOST` | 服务器 IP | `123.45.67.89` |
| `REMOTE_USER` | 服务器用户名 | `ubuntu` |
| `REMOTE_PORT` | SSH 端口 | `22` |
| `DEPLOY_PATH` | 部署路径 | `/home/ubuntu/homepage` |

**配置路径：** Settings → Secrets and variables → Actions → New repository secret

### 步骤 4：推送代码

```bash
git add .
git commit -m "启用自动部署"
git push origin master
```

---

## 📝 详细说明

查看 [QUICKSTART.md](QUICKSTART.md) 获取快速指南。

## 🔧 管理命令

```bash
# 查看服务状态
sudo systemctl status homepage

# 查看日志
sudo journalctl -u homepage -f

# 重启服务
sudo systemctl restart homepage
```
