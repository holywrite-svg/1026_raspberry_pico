#這是大綱
##這是次大綱
###這是次次大綱

```bash
git config --global user.name "Dean"
git config --global user.email "holywrite@gmail.com"
git config --global pull.rebase false
```

## 如何同步到 GitHub

### 方法 1：使用 GitHub Personal Access Token（推荐）

1. 生成 Token：
   - 访问 https://github.com/settings/tokens
   - 点击 "Generate new token (classic)"
   - 勾选 `repo` 权限
   - 复制生成的 token

2. 使用 token 推送：
   ```bash
   git push -u origin main
   ```
   当提示输入密码时，使用 token（不是你的 GitHub 密码）

### 方法 2：配置 SSH 密钥

1. 生成 SSH 密钥（如果还没有）：
   ```bash
   ssh-keygen -t ed25519 -C "your_email@example.com"
   ```

2. 将公钥添加到 GitHub：
   - 复制 `~/.ssh/id_ed25519.pub` 的内容
   - 访问 https://github.com/settings/keys
   - 点击 "New SSH key"，添加公钥

3. 更改远程 URL 为 SSH：
   ```bash
   git remote set-url origin git@github.com:holywrite-svg/1026_raspberry_pico.git
   ```

4. 推送：
   ```bash
   git push -u origin main
   ```

### 方法 3：使用 GitHub CLI

如果已安装 `gh`：
```bash
gh auth login
git push -u origin main
```

### 基本同步命令

- 提交更改：
  ```bash
  git add .
  git commit -m "提交信息"
  ```

- 推送到 GitHub：
  ```bash
  git push origin main
  ```

- 从 GitHub 拉取更新：
  ```bash
  git pull origin main
  ```