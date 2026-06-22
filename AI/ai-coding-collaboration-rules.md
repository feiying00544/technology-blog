# AI Coding Collaboration Rules

把一套个人编程协作规则（语言、代码修改、安全红线、验证结果、个人习惯）整理成 Claude Code、OpenAI Codex、GitHub Copilot 都能读懂的规则，并给出三家工具的全局落地方式。

> 口诀：**解释说人话，技术信息保留原样。**
> 知识截止 **2026-06-22**。三家工具的约定文件路径与格式来自官方文档核查，详见 [Agent / Skill / MCP / Workflow Guide](agent-skill-mcp-workflow-guide.md) 第四节。

---

## 一、五组规则

这套规则与本机两处全局文件（Claude Code 的 `CLAUDE.md`、Copilot CLI 的 `copilot-instructions.md`）**实质同源**，维护时请保持同步。

| 规则 | 要点 | 为什么 |
|------|------|--------|
| **语言规则** | 聊需求、讲原因、报结果用中文；代码、命令、变量名、报错信息保留英文原样 | 解释要说人话；报错原文是英文，保留它定位更准、自己 Google / 搜 issue 也方便 |
| **代码修改** | 框住手脚，只解决当前问题；不写"以后可能用得上"的代码；一次尽量只改一处；改完说明具体改了什么 | 防止修小毛病时顺手动一堆不相关代码 |
| **安全红线** | 密钥不进代码、`.env` 不上传、日志不含隐私；删库 / 批量删文件 / 上传数据 / 动外部接口 / 操作账号必须先确认再执行 | 很多操作没有撤销键，这是防止"理解错了还高效执行错误操作" |
| **验证结果** | 自称"修好了"不算数，必须测试（能否跑、旧 bug 在不在）；报错如实说、测试失败不隐瞒；修 bug 先写能复现的测试 | 要的是项目真正落地，不是好看的结果 |
| **个人习惯** | 服务端软件开发工程师；安全小事可直接操作；熟悉任务优先调用已装 Skill；删文件 / 密钥 / 上传外部资料先确认 | 把个人定位与边界固化，减少反复说明 |

---

## 二、三家工具的全局落地

三家都遵循"全局做基线、项目就近覆盖"的**继承 / 合并**模型：项目文件未写的规则仍继承全局，只有项目里**显式写了相反规则**时才在该点覆盖全局。

| 工具 | 全局文件 | 格式 | 继承 / 合并行为 |
|------|----------|------|-----------------|
| **Claude Code** | `~/.claude/CLAUDE.md` | Markdown，无 frontmatter | 全局做基线，项目根 / 子目录 `CLAUDE.md` 追加；冲突点项目就近覆盖 |
| **GitHub Copilot CLI** | `~/.copilot/copilot-instructions.md` | plain Markdown，无 frontmatter | 与仓库级 `.github/copilot-instructions.md` 同时生效；冲突时非确定性，官方建议避免冲突 |
| **OpenAI Codex** | `~/.codex/AGENTS.md` | Markdown，**无 frontmatter** | `AGENTS.md` 按目录就近生效，越近越权威；不冲突的全局条目继续继承 |

> 本机现状：Claude Code 与 Copilot CLI 已落地；**Codex 本次未在本机创建** `~/.codex/AGENTS.md`，需要时照下方片段放置即可。

---

## 三、各家格式片段（可直接复制）

三段内容实质一致，仅按各家约定调整文件位置与格式。

### Claude Code — 追加到 `~/.claude/CLAUDE.md`

```markdown
# 个人编程协作规则（全局）

## 语言规则
- 聊需求、讲原因、报结果用中文；代码、命令、变量名、报错信息保留英文原样。

## 代码修改
- 框住手脚，只解决当前问题；一次尽量只改一处；改完说明具体改了什么。

## 安全红线
- 密钥不进代码、.env 不上传、日志不含隐私；删库/批量删文件/上传数据/动外部接口/操作账号先确认再执行。

## 验证结果
- "修好了"必须经测试；报错如实说、测试失败不隐瞒；修 bug 先写能复现的测试。

## 个人习惯
- 服务端软件开发工程师；安全小事可直接操作；熟悉任务优先调用已装 Skill。
```

### GitHub Copilot CLI — 新建 `~/.copilot/copilot-instructions.md`

```markdown
# 个人编程协作规则（全局）

（小节同上：语言规则 / 代码修改 / 安全红线 / 验证结果 / 个人习惯）
```

> Copilot CLI 全局指令文件为 plain Markdown，与仓库级 `.github/copilot-instructions.md` 叠加生效。

### OpenAI Codex — 新建 `~/.codex/AGENTS.md`

```markdown
# 个人编程协作规则

（小节同上；Codex 的 AGENTS.md 不带 frontmatter，按目录就近合并）
```

---

## 四、维护约定

- 五组规则以本文档为单一事实来源；改动后同步更新两处全局文件（及需要时的 Codex `AGENTS.md`）。
- 时效性内容（路径、字段、命令）以最新官方文档为准；本次核查见 [Agent / Skill / MCP / Workflow Guide](agent-skill-mcp-workflow-guide.md)。

> **时效与诚信声明**：本文知识截止 2026-06-22。Copilot CLI 全局指令路径 `~/.copilot/copilot-instructions.md` 与 plain Markdown 格式来自 docs.github.com/copilot 官方文档核查；AI 工具迭代很快，落地前请以最新官方文档为准。
