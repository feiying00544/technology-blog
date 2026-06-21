---
name: p4-code-review
description: Review a Perforce changelist (CL) with project-aware checks. Use when asked to run /p4-code-review or review a Perforce CL number.
---

# Perforce Code Review

Review a Perforce changelist (CL) with project-aware checks.

## Usage

```
/p4-code-review <CL_NUMBER>
```

## Instructions

You are a code reviewer for a Perforce-managed project. Given a CL number provided by the user as the command argument, perform a thorough code review following these steps.

> **Output language (输出语言)**: The final review report — all findings, summaries, and the verdict — **must be presented in the language configured in `.claude/review-config.md` (`Output Language` field). If that field is absent, default to Simplified Chinese (简体中文).** This applies regardless of the language used in the code, CL description, or config files. Technical identifiers (class names, file paths, config keys, method names, log lines) are kept verbatim in their original form — only the prose around them is translated.

### Step 1: Gather CL Information

1. Run `p4 describe -S <CL>` to get the shelved diff (preferred), or `p4 describe -du <CL>` for submitted CLs.
2. Identify all affected files and their change types (add/edit/delete/integrate).
3. Read the CL description to understand intent.

### Step 2: Load Project-Specific Review Config

Read the file `.claude/review-config.md` in the project root. This file contains:
- Project-specific review dimensions (e.g., killswitch consistency, config file cross-check, etc.)
- File pattern rules (which files need special attention)
- Known pitfalls specific to this codebase

If `.claude/review-config.md` does not exist, ask the user:
1. "What language should the review report be written in?" (default: 简体中文 / Simplified Chinese)
2. "What are the key review dimensions for this project?" (e.g., correctness, config consistency, security, performance)
3. "Are there specific file patterns or conventions that need cross-checking?" (e.g., regional config must match global, proto changes need regeneration)
4. "Any known pitfalls or common mistakes in this codebase?"

Save the answers to `.claude/review-config.md` for future reviews, including an `## Output Language` section at the top recording the answer to question 1.

### Step 3: Contextual Analysis

For each modified file:
1. Read the current version of the file from the working tree.
2. Understand the diff in context of the surrounding code.
3. If the change modifies a function/method signature, interface, or configuration key:
   - Find all callers/references in the codebase using grep/glob.
   - Verify no call sites will break.
4. If the change modifies configuration:
   - Check consistency with other config files (e.g., other regional configs, global config).
   - Verify the config keys are referenced somewhere in code.

### Step 4: Cross-File Consistency

1. Check if the change introduces duplicates or conflicts with existing definitions.
2. Verify that related files that should be updated together have all been included in the CL.
3. For config changes: verify override/inheritance semantics are correct.

### Step 5: Compile/Build Impact

1. Determine if the changes could cause compilation errors (type changes, removed methods, etc.).
2. For config-only changes: verify HOCON/JSON/XML syntax is valid.
3. Check if proto/schema changes require regeneration steps.

### Step 6: Optimization Suggestions

After identifying issues, suggest:
1. A simpler or more minimal way to achieve the same goal.
2. Whether the change scope is appropriate (too broad? missing files?).
3. Potential maintenance/drift risks.

### Step 7: Output Format

Present the final review **in the configured output language (default 简体中文)**. Keep technical identifiers (file paths, class/method names, config keys) verbatim. Use this template (Chinese default shown):

```
## CL <编号> 代码评审总结

**变更说明**：<用一句话概括这个 CL 做了什么>
**改动文件**：<数量及清单>
**风险等级**：低 / 中 / 高

### 发现的问题

#### [阻断 / 警告 / 提示] <标题>
- **文件**：<path>
- **问题**：<问题描述>
- **影响**：<会破坏什么 / 可能出什么问题>
- **建议**：<如何修复>

### 交叉引用检查
- <已核对的调用方 / 引用清单>
- <发现的失效引用，如有>

### 编译 / 构建影响
- <能否编译通过？是否缺少依赖或需要重新生成？>

### 优化建议
- <更简洁的实现方式，如有>

### 评审结论
- [ ] 可以提交（Ready to submit）
- [ ] 需要修改（列出阻断项）
- [ ] 需要讨论（列出待澄清的问题）
```

> 严重级别对照：**阻断 = Critical**、**警告 = Warning**、**提示 = Info**。若 `Output Language` 配置为英文或其它语言，则按对应语言输出，模板结构保持一致。
