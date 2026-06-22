---
name: code-review
description: Review a Perforce CL, Git PR/MR, or commit with project-aware checks. Use when asked to run /code-review, review a CL, inspect a PR, or evaluate a code change.
---

# code-review

Perform a thorough, evidence-based code review for a Perforce CL, Git PR/MR, or commit.

In this repository, Perforce CL review is the primary path. Prefer project-specific rules from `.claude/review-config.md` when present, and also read `.github/copilot-instructions.md` for repository background.

## Input handling

The user's input after `/code-review` is the change identifier:

- Perforce changelist number, such as `720624`
- GitHub/GitLab PR or MR number, URL, `#1234`, `PR-1234`, or `!1234`
- Git commit hash
- Multiple identifiers, reviewed one by one

If no identifier is provided, ask the user to provide one and stop.

## Step 0: Load project context

1. Read `.github/copilot-instructions.md` if it exists.
2. Read `.claude/review-config.md` if it exists.
3. Extract:
   - VCS and review platform
   - project-specific review dimensions
   - multi-environment or SKU rules
   - build and test behavior
   - output language
4. If both files are missing, continue with the generic checklist and clearly state the reduced project context.

## Step 1: Gather change information

### Perforce

For a numeric CL, prefer shelved diff:

```powershell
p4 describe -S <CL> | Out-String
```

If the CL is submitted or shelved output is unavailable, also try:

```powershell
p4 describe -du <CL> | Out-String
p4 describe -s <CL> | Out-String
```

Record the CL description, author, affected files, action types, and diff hunks.
Save the full CL description text for Step 4.5 (CL Comment format check).

### GitHub or GitLab PR/MR

Use available tools in order:

```bash
gh pr view <num> --json title,body,author,files,headRefOid,baseRefName
gh pr diff <num>
glab mr view <num>
glab mr diff <num>
```

### Commit or local diff

Use:

```bash
git --no-pager show --stat <sha>
git --no-pager show <sha>
git --no-pager diff <base>...<head>
```

If no tool can fetch the diff, ask the user for the diff text or review URL.

## Step 2: Classify the change

Tag each changed area as appropriate:

- bug fix
- business logic
- API or schema change
- cache, persistence, or message format
- configuration or multi-environment behavior
- performance or concurrency
- security or authorization
- observability
- tests

## Step 3: Read enough context

For every meaningful changed file:

1. Read the current file around the changed area.
2. Search for all references to changed public/protected methods, constructors, config keys, cache keys, REST paths, message schemas, and proto fields.
3. For new helper or utility calls introduced by the diff, read their definitions before making claims about return values, nullability, exceptions, or side effects.
4. For config or SKU changes, compare related regional/environment files according to `.github/copilot-instructions.md` and `.claude/review-config.md`.
5. For large changes, delegate independent context-gathering tasks to subagents if available.

## Step 4: Review checklist

Apply both project-specific checks and this generic checklist:

- Compatibility: public/protected API signatures, constructors, interfaces, serialized fields, DB schemas, protobufs, and external contracts.
- Correctness: condition changes, edge cases, error handling, nullability, and data migration.
- Concurrency and performance: locks, shared state, N+1 calls, loop complexity, and avoidable full scans.
- Security: authentication, authorization, input validation, path/SQL/command injection, and sensitive logs.
- Observability: actionable logs, metrics, traceability, and log level on high-frequency paths.
- Tests: whether the change has appropriate unit/integration coverage, and whether existing tests are skipped by default.
- Configuration: cross-region or cross-environment consistency and valid syntax.
- Reuse and maintainability: use existing helpers and keep logic consistent with surrounding code.

## Step 4.5: CL Comment 规范检查（仅 Perforce CL）

此步骤仅对 Perforce CL 生效，Git PR/MR 跳过。检查结果为 **Advisory（建议性）**，不影响"是否可合入"结论。

### 标准格式

```
#类型 >TTM< [功能模块][JASS号] 修改内容描述
JASS链接
Review链接
reviewed by 人名, pit by 人名
```

示例：

```
#feature >TTM< [NXCommand][FMG-385560] 1.add nxcommand to unequip playStyle from player card 2.add nxcommand to grant/revoke playStyle to/from inventory
https://jaas.ea.com/browse/FMG-385560
http://eamc-swarm1.eamobile.ad.ea.com/reviews/746886
reviewed by linwei, fengls, pit by shu,zhang
```

### 检查要素

| # | 要素 | 规则 |
|---|------|------|
| 1 | 类型标记 | 首行须以 `#feature`、`#fix`、`#refactor`、`#config` 等类型标记开头 |
| 2 | >TTM< 标记 | 若分支名含 `RL` 或 `Stage`（不区分大小写），则首行须包含 `>TTM<` |
| 3 | 功能模块 | 首行须包含 `[模块名]`，如 `[NXCommand]`、`[LiveOps]` |
| 4 | JASS 工单号 | 首行须包含 `[FMG-XXXXXX]` 格式的工单号 |
| 5 | 修改内容描述 | 首行工单号之后须有实际修改内容的文字说明 |
| 6 | JASS 链接 | 须包含 `https://jaas.ea.com/browse/FMG-*` 链接，且工单号与首行一致 |
| 7 | Review 链接 | 须包含 Swarm review URL（`http://eamc-swarm1.eamobile.ad.ea.com/reviews/*`） |
| 8 | reviewed by / pit by | 须包含 `reviewed by` 和 `pit by` 及具体人名 |

### 判定

- 逐项检查，缺失或不符的要素标记为 ⚠️，符合的标记为 ✅
- 整体 comment 合规度以"X/8 项通过"汇总
- **再次强调：此检查结果不纳入"是否可合入"的判断**

## Step 5: Validate when feasible

- For code changes, run the most targeted existing build, type-check, linter, or tests that are practical for the affected module.
- For config-only changes, validate syntax where tooling exists.
- If validation cannot be run, say so in the review confidence section.

## Step 6: Output report

Use the output language from `.claude/review-config.md` `## Output Language`; default to Simplified Chinese.

Each finding must include:

- file and line number
- severity: Blocker, Major, Minor, or Nit
- category
- factual evidence
- concrete recommendation

Use this structure:

```markdown
# Code Review: <标识>

## 概要

- 主题：...
- 改动文件：...
- 风险等级：低 / 中 / 高

## ✅ 合理改动

- ...

## ⚠️ 需要改进

### 1. [Blocker/Major/Minor/Nit] <文件:行号> — <标题>

- **分类**：...
- **现象**：...
- **建议**：...
- **理由**：...

## 📝 CL Comment 规范检查（Advisory，不影响合入判断）

| # | 要素 | 状态 | 说明 |
|---|------|------|------|
| 1 | 类型标记 | ✅/⚠️ | ... |
| 2 | >TTM< | ✅/⚠️/N/A | ... |
| 3 | 功能模块 | ✅/⚠️ | ... |
| 4 | JASS 工单号 | ✅/⚠️ | ... |
| 5 | 修改内容描述 | ✅/⚠️ | ... |
| 6 | JASS 链接 | ✅/⚠️ | ... |
| 7 | Review 链接 | ✅/⚠️ | ... |
| 8 | reviewed by / pit by | ✅/⚠️ | ... |

合规度：X/8 项通过

## 📋 总评 / 是否可合入

...

## 🔍 评审置信度

- [ ] 静态阅读全部改动文件
- [ ] 核验签名变更影响面
- [ ] 核验新增 helper 契约
- [ ] 追踪跨模块 producer/consumer 或配置影响
- [ ] 运行相关验证，或说明未运行原因
```

## Constraints

- Do not modify source code while reviewing.
- Do not report speculative findings; every issue needs evidence from the diff or repository context.
- Do not comment on trivial style unless it affects correctness, compatibility, maintainability, or project conventions.
- Keep the skill portable; project-specific facts belong in `.github/copilot-instructions.md` or `.claude/review-config.md`.
