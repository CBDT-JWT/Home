# ✅ 已更新为 SSH Deploy Action

## 🔄 变更说明

配置已从旧版本更新为使用 `easingthemes/ssh-deploy@main`。

---

## 主要变化

### 旧版配置 ❌

```yaml
- name: Deploy to Ubuntu Server
  uses: appleboy/ssh-action@v1.0.0
  with:
    host: ${{ secrets.SERVER_HOST }}
    username: ${{ secrets.SERVER_USER }}
    key: ${{ secrets.SERVER_SSH_KEY }}
    port: ${{ secrets.SERVER_PORT }}
    script: |
      cd ${{ secrets.DEPLOY_PATH }}
      git pull origin main
      ...
```

### 新版配置 ✅

```yaml
- name: Deploy to Server via SSH
  uses: easingthemes/ssh-deploy@main
  with:
    SSH_PRIVATE_KEY: ${{ secrets.SSH_PRIVATE_KEY }}
    REMOTE_HOST: ${{ secrets.REMOTE_HOST }}
    REMOTE_USER: ${{ secrets.REMOTE_USER }}
    REMOTE_PORT: ${{ secrets.REMOTE_PORT }}
    TARGET: ${{ secrets.DEPLOY_PATH }}
    EXCLUDE: "/deploy/, /.git/, /.github/, /venv/, ..."
    SCRIPT_AFTER: |
      cd ${{ secrets.DEPLOY_PATH }}
      python3 -m venv venv
      ...
```

---

## GitHub Secrets 变更

### 旧的 Secret 名称 → 新的 Secret 名称

| 旧名称 | 新名称 | 说明 |
|-------|--------|------|
| `SERVER_HOST` | `REMOTE_HOST` | 服务器地址 |
| `SERVER_USER` | `REMOTE_USER` | 用户名 |
| `SERVER_SSH_KEY` | `SSH_PRIVATE_KEY` | SSH 私钥 |
| `SERVER_PORT` | `REMOTE_PORT` | SSH 端口 |
| `DEPLOY_PATH` | `DEPLOY_PATH` | ✅ 保持不变 |

---

## ⚠️ 需要做的事情

### 如果你之前配置了旧的 Secrets：

**选项 1：重命名现有 Secrets**

你需要在 GitHub 删除旧的 Secrets，创建新的：

1. 进入 `Settings → Secrets and variables → Actions`
2. 删除旧的：
   - `SERVER_HOST`
   - `SERVER_USER`
   - `SERVER_SSH_KEY`
   - `SERVER_PORT`
3. 创建新的（使用新名称）：
   - `REMOTE_HOST`
   - `REMOTE_USER`
   - `SSH_PRIVATE_KEY`
   - `REMOTE_PORT`
   - `DEPLOY_PATH`（如果还没有）

**选项 2：修改配置文件使用旧名称**

或者你也可以修改 `.github/workflows/ci-cd.yml` 使用旧的 Secret 名称：

```yaml
with:
  SSH_PRIVATE_KEY: ${{ secrets.SERVER_SSH_KEY }}
  REMOTE_HOST: ${{ secrets.SERVER_HOST }}
  REMOTE_USER: ${{ secrets.SERVER_USER }}
  REMOTE_PORT: ${{ secrets.SERVER_PORT }}
  TARGET: ${{ secrets.DEPLOY_PATH }}
```

---

## 🎯 推荐做法

**使用新的 Secret 名称**（选项 1），因为：
- ✅ 符合 SSH Deploy Action 的标准命名
- ✅ 更清晰明确
- ✅ 避免与其他 Actions 混淆

---

## 📝 配置步骤

详细配置请查看：
- [SECRETS_CONFIG.md](SECRETS_CONFIG.md) - Secrets 配置详解
- [QUICKSTART.md](QUICKSTART.md) - 快速开始指南
- [README.md](README.md) - 完整部署文档

---

## 🚀 验证部署

配置完成后：

```bash
git add .
git commit -m "update to ssh-deploy action"
git push origin master
```

然后在 GitHub Actions 页面查看部署状态。
