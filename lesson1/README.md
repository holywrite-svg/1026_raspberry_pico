-#這是大綱
-##這是次大綱
-###這是次次大綱

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

## Git 冲突的原因、发生情况与解决方法

### 冲突的原因

Git 冲突（Merge Conflict）发生在以下情况：

1. **分支历史偏离**：
   - 本地仓库和远程仓库有不同的提交历史
   - 同一个文件的同一部分在不同分支上被修改
   - Git 无法自动决定应该保留哪个版本

2. **常见的冲突场景**：
   - 本地和远程同时修改了同一个文件的同一行或同一区域
   - 本地删除的文件在远程被修改
   - 远程删除的文件在本地被修改
   - 两个分支对同一文件进行了不同的修改

### 冲突是如何发生的（实际案例）

在我们的项目中，冲突是这样发生的：

1. **初始状态**：
   - 远程仓库（GitHub）已有一个初始提交，包含基本的 README.md 和 lesson1/README.md
   - 本地仓库也有自己的提交历史

2. **历史偏离**：
   ```
   本地分支：提交 A → 提交 B → 提交 C
   远程分支：提交 X（不同的历史起点）
   ```

3. **触发冲突的操作**：
   ```bash
   git pull origin main
   # 或
   git merge origin/main
   ```

4. **Git 无法自动合并**：
   - README.md：本地添加了"每日上課連結"文本，远程没有这行
   - lesson1/README.md：本地添加了完整的 GitHub 同步说明，远程只有基本的 git config
   - Git 标记为冲突，需要手动解决

5. **错误信息示例**：
   ```
   您的分支和 'origin/main' 出現了偏離，
   並且分別有 2 和 1 處不同的提交。
   
   衝突（新增/新增）：合併衝突於 README.md
   衝突（新增/新增）：合併衝突於 lesson1/README.md
   自動合併失敗，修正衝突然後提交修正的結果。
   ```

### 冲突标记说明

当 Git 检测到冲突时，会在文件中插入冲突标记：

```
<<<<<<< HEAD
这是本地版本的代码
=======
这是远程版本的代码
>>>>>>> 957a2f4d5e90c4a4b9f1d5aeaf61843b3fb8916f
```

- `<<<<<<< HEAD`：标记冲突开始，后面是本地（当前分支）的版本
- `=======`：分隔本地和远程版本
- `>>>>>>> commit_hash`：标记远程版本结束，commit_hash 是远程提交的哈希值

### 解决冲突的步骤

#### 步骤 1：查看冲突状态
```bash
git status
```
输出示例：
```
未合併的路徑：
  雙方新增：   README.md
  雙方新增：   lesson1/README.md
```

#### 步骤 2：检查冲突文件
```bash
# 查看有冲突的文件列表
git diff --name-only --diff-filter=U

# 查看具体冲突内容
cat README.md
cat lesson1/README.md
```

#### 步骤 3：手动解决冲突

打开冲突文件，找到冲突标记，选择要保留的内容：

**选项 A：保留本地版本**
```
<<<<<<< HEAD
本地内容
=======
远程内容
>>>>>>> commit_hash
```
改为：
```
本地内容
```

**选项 B：保留远程版本**
```
<<<<<<< HEAD
本地内容
=======
远程内容
>>>>>>> commit_hash
```
改为：
```
远程内容
```

**选项 C：合并两个版本**（推荐）
```
<<<<<<< HEAD
本地内容1
=======
远程内容1
>>>>>>> commit_hash
```
改为：
```
本地内容1
远程内容1
```

#### 步骤 4：标记冲突已解决
```bash
# 将解决后的文件添加到暂存区
git add README.md lesson1/README.md

# 或者一次性添加所有已解决的文件
git add .
```

#### 步骤 5：完成合并提交
```bash
git commit -m "Merge remote-tracking branch 'origin/main' - 解决冲突"
```

#### 步骤 6：推送到远程
```bash
git push origin main
```

### 完整的冲突解决流程示例

```bash
# 1. 尝试拉取远程更改
git pull origin main

# 2. 如果出现冲突，查看状态
git status

# 3. 手动编辑冲突文件，移除冲突标记，保留需要的内容

# 4. 标记冲突已解决
git add <冲突文件>

# 5. 完成合并
git commit -m "解决合并冲突"

# 6. 推送到远程
git push origin main
```

### 处理"拒绝合并无关历史"错误

如果遇到以下错误：
```
致命錯誤: 拒絕合併無關的歷史
```

解决方法：
```bash
git pull origin main --allow-unrelated-histories
```

这个选项允许 Git 合并两个完全独立的提交历史。

### 预防冲突的最佳实践

1. **频繁同步**：
   ```bash
   # 推送前先拉取
   git pull origin main
   git push origin main
   ```

2. **小步提交**：
   - 不要累积太多更改再提交
   - 每次提交解决一个小问题

3. **与团队沟通**：
   - 修改文件前告知团队成员
   - 避免多人同时修改同一文件

4. **使用分支**：
   ```bash
   # 创建功能分支
   git checkout -b feature-branch
   
   # 开发完成后合并
   git checkout main
   git merge feature-branch
   ```

5. **定期拉取**：
   ```bash
   # 每天开始工作前拉取最新更改
   git pull origin main
   ```

### 取消合并（如果出错）

如果合并过程中出错，想回到合并前的状态：
```bash
git merge --abort
```

这会取消当前的合并操作，恢复到合并前的状态。

### 实际案例总结

在我们的项目中：
- **冲突文件**：README.md 和 lesson1/README.md
- **冲突类型**：双方新增（两个分支都添加了新内容）
- **解决方法**：合并两个版本的内容，保留所有有价值的信息
- **最终结果**：成功合并本地和远程的更改，保留了完整的文档内容
