# Git 仓库管理 (Git Manager)

用于管理本地 Git 仓库的 Skill，支持常见的 Git 操作。

## 功能

- ✅ 查看仓库状态
- ✅ 查看提交历史
- ✅ 查看分支
- ✅ 查看差异
- ✅ 添加和提交更改
- ✅ 推送和拉取
- ✅ 创建和管理分支
- ✅ 查看文件变更

## 常用命令

### 仓库状态

```bash
# 查看仓库状态
git status

# 查看当前分支
git branch

# 查看详细状态
git status -s
```

### 提交历史

```bash
# 查看最近提交
git log --oneline -10

# 查看提交历史（含变更
git log -p -1

# 简略统计
git shortlog -sn
```

### 分支管理

```bash
# 查看所有分支
git branch -a

# 创建新分支
git checkout -b feature/xxx

# 切换分支
git checkout main

# 删除分支
git branch -d branch_name
```

### 更改管理

```bash
# 查看未暂存的变更
git diff

# 查看已暂存的变更
git diff --cached

# 查看特定文件变更
git diff file_path
```

### 暂存和提交

```bash
# 添加所有更改
git add .

# 添加特定文件
git add file_path

# 提交更改
git commit -m "commit message"

# 添加并提交
git commit -am "message"
```

### 远程操作

```bash
# 拉取最新
git pull

# 推送到远程
git push

# 推送到特定分支
git push origin branch_name

# 查看远程仓库
git remote -v
```

### 文件操作

```bash
# 查看文件在哪些提交中修改过
git log --oneline file_path

# 查看文件的变更历史
git log -p file_path

# 恢复文件到上次提交的状态
git checkout -- file_path

# 查看特定版本的文件内容
git show commit:file_path
```

## 实用技巧

### 快速查看状态

```bash
# 简洁状态
git status -sb

# 显示分支和上游
git branch -vv
```

### 日志美化

```bash
# 图形化显示
git log --graph --oneline --all

# 今日提交
git log --since=midnight --author=$(git config user.email)
```

### 暂存操作

```bash
# 暂存当前工作
git stash

# 恢复暂存
git stash pop

# 查看暂存列表
git stash list
```

## 配置

### 用户信息

```bash
git config --global user.name "Your Name"
git config --global user.email "your@email.com"
```

### 别名

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg "log --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --abbrev-commit"
```

## 示例输出

```
$ git status -sb
## main
 M modified_file.txt
?? new_file.txt

$ git log --oneline -5
abc1234 Last commit message
def5678 Second to last commit
ghi9012 Third commit
jkl3456 Fourth commit
mno7890 Fifth commit
```

## 注意事项

- 提交前务必确认变更内容
- 推送前先拉取最新代码
- 重要操作前建议创建备份分支
- 使用有意义的提交信息

## GitHub 配置

### 已配置的远程仓库

```
origin https://github.com/jiaruoruo/openclaw-robot.git (已认证)
```

### 推送命令

```bash
# 推送到 GitHub
git push -u origin master

# 推送所有分支
git push --all origin
```

### 配置 GitHub Token (如需重新配置)

```bash
# 方法1: 使用 token 作为远程 URL
git remote set-url origin https://YOUR_TOKEN@github.com/username/repo.git

# 方法2: 使用 git credential store
git config --global credential.helper store
# 下次推送时输入用户名和 token

# 方法3: 使用环境变量
# GIT_ASKPASS=echo GIT_TERMINAL_PROMPT=0 git push
```

### GitHub Token 安全提示

- ⚠️ 切勿将 token 提交到代码仓库
- 建议使用 GitHub CLI 或 credential helper 管理凭据
- 定期轮换 token
