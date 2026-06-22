# dev-language-polisher 使用与迁移说明

`dev-language-polisher` 是一个可迁移的 `SKILL.md` 能力，用于把中文或英文的开发沟通文本翻译并润色为自然、正式的美式英语，并修复原文中的语法和拼写错误。

它的主输出是一段忠实、自然的翻译；当原文是开发变更/任务描述时，再补充按用途分类的表达。

它会使用适合 IDE Chat 自动换行的 Markdown 分区输出：

**翻译（Translation）：**

> 忠实、自然且语法正确的美式英语翻译。

当原文是开发变更/任务描述时，补充：

**作为 Jira Task / Story Title（推荐）：**

> 适合作为 Jira task 或 story 标题的英文表达。

**作为 Git Commit Message：**

> 适合作为 Git commit message 的英文表达。

**作为 Release Note 或项目成果描述：**

> 适合作为 release note、项目成果描述或状态总结的英文表达。

**其中：**

- 用中文说明语法修复、错别字、词语选择和语气差异。
- 如果内容较长，会按语义拆成短段落或短列表。

该格式不会把最终结果放入代码块，避免 IDEA 或 VS Code 的 Chat 面板出现横向滚动条。

## 保留的文件

当前只保留 skill 相关文件：

```text
.github\skills\dev-language-polisher\SKILL.md
.github\skills\dev-language-polisher\USAGE.md
.claude\skills\dev-language-polisher\SKILL.md
```

其中：

- `.github\skills\dev-language-polisher\SKILL.md` 供 GitHub Copilot CLI 使用。
- `.claude\skills\dev-language-polisher\SKILL.md` 供 Claude Code 使用。
- `.github\skills\dev-language-polisher\USAGE.md` 是本说明文档。

## 在 GitHub Copilot CLI 中使用

添加或修改 skill 后，先重新加载：

```text
/skills reload
```

确认 skill 是否可用：

```text
/skills info dev-language-polisher
```

直接调用 skill：

```text
Use the /dev-language-polisher skill to polish: I founded a bug in the deploy script, it can't works on windows.
```

也可以处理中文输入：

```text
Use the /dev-language-polisher skill to polish: 这个代码有个bug，我明天修一下可以吗
```

## 在 Claude Code 中使用

直接调用 skill：

```text
/dev-language-polisher I founded a bug in the deploy script, it can't works on windows.
```

处理中文输入：

```text
/dev-language-polisher 这个代码有个bug，我明天修一下可以吗
```

如果 Claude Code 启动时还不存在 `.claude\skills` 目录，需要重启 Claude Code 后再使用。若目录已存在，通常修改 `SKILL.md` 后会自动生效。

## 迁移到其它项目

在目标项目根目录执行以下 PowerShell 命令。请先把 `$sourceRepo` 改为当前项目或模板项目的实际路径：

```powershell
$sourceRepo = "d:\path\to\source-repo"

New-Item -ItemType Directory -Force .github\skills | Out-Null
New-Item -ItemType Directory -Force .claude\skills | Out-Null

Copy-Item -Recurse "$sourceRepo\.github\skills\dev-language-polisher" .github\skills\
Copy-Item -Recurse "$sourceRepo\.claude\skills\dev-language-polisher" .claude\skills\
```

迁移完成后：

- Copilot CLI 中执行 `/skills reload`。
- Claude Code 如未自动识别，重启 Claude Code。

## 安装为个人全局 skill

如果希望所有项目都能使用该 skill，可以安装到用户目录。

Copilot CLI：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.copilot\skills" | Out-Null
Copy-Item -Recurse .github\skills\dev-language-polisher "$env:USERPROFILE\.copilot\skills\"
```

Claude Code：

```powershell
New-Item -ItemType Directory -Force "$env:USERPROFILE\.claude\skills" | Out-Null
Copy-Item -Recurse .claude\skills\dev-language-polisher "$env:USERPROFILE\.claude\skills\"
```

安装完成后：

- Copilot CLI 中执行 `/skills reload`。
- Claude Code 如未自动识别，重启 Claude Code。

## 维护方式

维护时请保持以下两个文件内容同步：

```text
.github\skills\dev-language-polisher\SKILL.md
.claude\skills\dev-language-polisher\SKILL.md
```

如果修改了输出格式、规则或示例，请同时更新两个 `SKILL.md` 文件，并检查本说明文档中的使用示例是否仍然准确。
