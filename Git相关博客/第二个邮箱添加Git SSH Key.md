## 为第二个邮箱添加 SSH Key（Windows & Mac）

### 1. 生成新密钥

```bash
ssh-keygen -t ed25519 -C "second@example.com" -f ~/.ssh/id_second
-t ed25519：使用 Ed25519 椭圆曲线算法（密钥短、安全性高、速度快，推荐）
-C：备注（通常填邮箱）
-f：指定文件名，避免覆盖已有 key
示例（实际生成的密钥文件为 id_xxxxxx）：


ssh-keygen -t ed25519 -C "xxxxxx@gmail.com" -f ~/.ssh/id_xxxxxx
2. 将公钥添加到 GitHub/GitLab

cat ~/.ssh/id_xxxxxx.pub
复制输出内容，粘贴到平台的 Settings → SSH Keys 中。

3. 配置 SSH config
编辑 ~/.ssh/config（不存在则新建）：


# 第一个账号（已有）
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_ed25519

# 第二个账号
Host github-second
  HostName github.com
  User git
  IdentityFile ~/.ssh/id_xxxxxx
4. 将私钥加入 ssh-agent
Mac：


eval "$(ssh-agent -s)"
ssh-add ~/.ssh/id_xxxxxx
可在 ~/.ssh/config 中加 AddKeysToAgent yes 实现自动加载。

Windows（PowerShell 管理员）：


# 设置 ssh-agent 服务为自动启动
Get-Service ssh-agent | Set-Service -StartupType Automatic

# 启动 ssh-agent 服务
Start-Service ssh-agent

# 添加密钥
ssh-add $env:USERPROFILE\.ssh\id_xxxxxx

# 验证已加载的密钥
ssh-add -l
使用 Windows OpenSSH 服务方式添加的密钥会持久保留，重启后无需重新添加。

5. 使用
克隆第二个账号的仓库时，使用 config 中定义的 Host 别名：


git clone git@github-second:username/repo.git
已有仓库修改 remote：


git remote set-url origin git@github-second:username/repo.git
6. 验证

ssh -T git@github.com          # 第一个账号
ssh -T git@github-second       # 第二个账号

