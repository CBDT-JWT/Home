# GitHub Secrets 配置对照表

## 需要配置的 Secrets

在 GitHub 仓库中配置以下 5 个 Secrets：

**路径：** `仓库 → Settings → Secrets and variables → Actions → New repository secret`

---

## Secrets 列表

### 1. SSH_PRIVATE_KEY

**说明：** SSH 私钥完整内容

**获取方式：**
```bash
# 在服务器上执行
cat ~/.ssh/github_deploy
```

**格式：**
```
-----BEGIN OPENSSH PRIVATE KEY-----
b3BlbnNzaC1rZXktdjEAAAAABG5vbmUAAAAEbm9uZQAAAAAAAAABAAAAMwAAAAtzc2gtZW
...（完整私钥内容）...
-----END OPENSSH PRIVATE KEY-----
```

⚠️ **重要：** 必须包含开始和结束标记行

---

### 2. REMOTE_HOST

**说明：** 服务器 IP 地址或域名

**获取方式：**
```bash
# 在服务器上执行
curl ifconfig.me
```

**示例：**
```
123.45.67.89
```

或域名：
```
example.com
```

---

### 3. REMOTE_USER

**说明：** 服务器登录用户名

**获取方式：**
```bash
# 在服务器上执行
whoami
```

**示例：**
```
ubuntu
```

或
```
your_username
```

---

### 4. REMOTE_PORT

**说明：** SSH 端口号

**默认值：**
```
22
```

如果修改了 SSH 端口，填写对应端口号。

---

### 5. DEPLOY_PATH

**说明：** 服务器上的部署目录绝对路径

**获取方式：**
```bash
# 在服务器上执行
echo "/home/$(whoami)/homepage"
```

**示例：**
```
/home/ubuntu/homepage
```

或
```
/home/your_username/homepage
```

---

## 配置步骤

1. 进入 GitHub 仓库页面
2. 点击 **Settings** (设置)
3. 左侧菜单选择 **Secrets and variables** → **Actions**
4. 点击 **New repository secret** (新建仓库密钥)
5. 填写 Name 和 Secret 内容
6. 点击 **Add secret** (添加密钥)
7. 重复步骤 4-6，添加所有 5 个密钥

---

## 验证配置

配置完成后，推送代码：

```bash
git add .
git commit -m "test deploy"
git push origin master
```

然后在 GitHub Actions 页面查看部署进度。

---

## 常见错误

### ❌ SSH 连接失败
- 检查 `SSH_PRIVATE_KEY` 格式是否完整
- 确认 `REMOTE_HOST` 和 `REMOTE_PORT` 正确
- 验证公钥已添加到服务器：`cat ~/.ssh/authorized_keys`

### ❌ 权限错误
- 确保 `REMOTE_USER` 对 `DEPLOY_PATH` 有写权限
- 检查 sudoers 配置：`sudo visudo`

### ❌ 路径不存在
- 确认 `DEPLOY_PATH` 在服务器上已创建
- 运行初始化脚本：`deploy/setup.sh`

---

## 快速测试

```bash
# 测试 SSH 连接
ssh REMOTE_USER@REMOTE_HOST -p REMOTE_PORT

# 测试路径访问
ssh REMOTE_USER@REMOTE_HOST "ls -la DEPLOY_PATH"
```

替换大写变量为实际值。
