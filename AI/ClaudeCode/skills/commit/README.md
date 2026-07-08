# Claude Code Commit Skill

自动读取项目 CLAUDE.md 中的 commit 规范，推断 Action/Module，确认后执行提交。

---

## 功能

- 自动识别项目 commit 规范（从 CLAUDE.md 读取），无规范时 fallback 到 Conventional Commits
- 从 diff 推断 Action（Add/Modify/Remove/Fix）和 Module（从变更路径提取）
- 提交前展示拟 stage 文件列表和 commit message，等待用户确认
- 支持过滤条件（如 `/commit only md files`）
- 禁止 Co-Authored-By trailer

## 安装

### 1. 复制 Skill

将 `SKILL.md` 复制到全局或项目级 skill 目录：

```bash
# global (all projects)
mkdir -p ~/.claude/skills/commit
cp SKILL.md ~/.claude/skills/commit/SKILL.md

# project-level (single project)
mkdir -p .claude/skills/commit
cp SKILL.md .claude/skills/commit/SKILL.md
```

### 2. 配置 PreToolUse Hook（可选，推荐）

Hook 会在 `git commit` 执行前校验 message 格式，不符合规范的提交将被拦截。

**2a.** 复制 hook 脚本到项目：

```bash
mkdir -p .claude/hooks
cp hooks/validate-commit-msg.py .claude/hooks/validate-commit-msg.py
```

**2b.** 在项目的 `.claude/settings.local.json`（或 `.claude/settings.json`）中添加 hook 配置：

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python .claude/hooks/validate-commit-msg.py"
          }
        ]
      }
    ]
  }
}
```

> **注意：** hook 脚本中的格式正则 `^\[(Fix|Modify|Add|Remove)\]\[[A-Za-z,]+\].+` 是针对 `[Action][Module]Summary` 规范的。如果你的项目使用其他 commit 规范（如 Conventional Commits），需修改 `validate-commit-msg.py` 中的 `pattern` 变量。

### 3. 前置依赖

- Python 3（用于 hook 脚本的 JSON 解析）
- 项目 CLAUDE.md 中包含 commit 规范段落（标题含 "Git Commit" 或 "Commit"）

## 使用

```
/commit                          # 提交所有变更
/commit only md files            # 只提交 .md 文件
/commit only AI/ directory       # 只提交 AI/ 目录下的变更
```

Skill 会展示拟提交文件和 message，确认后执行。

## 文件说明

```
commit/
├── SKILL.md                        # Skill 定义文件（复制到 ~/.claude/skills/commit/）
├── hooks/
│   └── validate-commit-msg.py      # PreToolUse hook 脚本（复制到项目 .claude/hooks/）
└── README.md                       # 本文件
```
