---
name: init-project
description: Scan the current workspace and generate or update .github/copilot-instructions.md with project-specific Copilot guidance. Use when asked to initialize project instructions, refresh repository context, or replace the legacy project initialization prompt workflow.
---

# init-project

Initialize or refresh the repository-level Copilot instructions file at `.github/copilot-instructions.md`.

This current-format project skill is named `init-project` so it does not conflict with the Copilot CLI built-in `/init` command.

## Input handling

- If the user provides no extra instructions, scan the current workspace root and produce Simplified Chinese output.
- If the user provides a subpath or focus area, sample that area first, but still scan root-level project marker files.
- If `.github/copilot-instructions.md` already exists, ask whether to overwrite, incrementally update, or cancel.

## Required workflow

1. Identify project type and technology stack.
   - Look for build and package files: `pom.xml`, `build.gradle*`, `build.sbt`, `package.json`, lockfiles, `go.mod`, `Cargo.toml`, `*.csproj`, `*.sln`, `CMakeLists.txt`, and `Makefile`.
   - Look for container, CI, documentation, VCS, and IDE/tooling markers.
   - Read the most important build files and README-style files.
2. Scan the directory structure.
   - Summarize root-level modules and key source directories.
   - Avoid guessing; base every module description on file names, README content, or directory contents.
3. Identify version control and collaboration flow.
   - Detect Git, Perforce, SVN, or other VCS markers.
   - Check for review templates, CODEOWNERS, and contribution docs.
4. Identify coding standards and validation tools.
   - Record linters, formatters, test frameworks, build profiles, and whether tests are skipped by default.
5. Identify observability, configuration, environments, and data stores.
   - Record logging frameworks, config formats, metrics/tracing systems, databases, queues, and variant mechanisms.
6. Ask only for information that cannot be detected automatically, such as internal project name, default branch, special review rules, or output language.
7. Generate `.github/copilot-instructions.md`.
   - Keep stable headings so other skills can read the file reliably:
     - `## 项目概要`
     - `## 技术栈`
     - `## 项目模块结构`
     - `## 编码规范`
     - `## 版本控制与协作`
     - `## 可观测性 / 配置 / 数据`
     - `## 项目专属注意事项`
     - `## 常用命令`
     - `## 可用的 Copilot Skill`
   - List current-format skills from `.github/skills/*/SKILL.md`.
8. Read the generated file back and check that the main sections are present.

## Output template

Use this skeleton, removing sections where there is no evidence:

~~~markdown
# GitHub Copilot Instructions — <项目名>

> 本文件由 `/init-project` skill 自动生成，作为本项目 Copilot skills 共享的背景知识。
> 最后更新：<YYYY-MM-DD>

## 项目概要

- 项目名 / 代号：...
- 一句话定位：...
- 主要语言：...
- 主要构建工具：...
- 版本控制：...
- 默认分支 / 主线：...

## 技术栈

| 类别 | 技术 / 版本 |
| --- | --- |
| 语言 | ... |
| 构建 | ... |
| 框架 | ... |
| 数据存储 | ... |
| 测试 | ... |
| 日志 / 监控 | ... |
| CI | ... |

## 项目模块结构

```text
<根目录>/
├── <模块A>/    # 职能
└── <模块B>/    # 职能
```

## 编码规范

- 命名 / 分层约定：...
- 自动检查工具：...
- 提交信息约定：...
- 测试约定：...

## 版本控制与协作

- VCS：...
- 评审平台：...
- CL / PR 命名 / 描述模板：...
- 关联工单系统：...

## 可观测性 / 配置 / 数据

- 配置文件位置与格式：...
- 多环境 / 多变体机制：...
- 日志框架与规范：...
- 监控 / 指标系统：...

## 项目专属注意事项

> 这里登记的是只在本项目适用、需要被其它 Copilot skills 感知的检查项与约束。

## 常用命令

```bash
# 构建 / 测试 / 运行命令
```

## 可用的 Copilot Skill

| Skill | 文件 | 作用 |
| --- | --- | --- |
| `/init-project` | `.github/skills/init-project/SKILL.md` | 生成或更新本文件 |
| `/code-review <改动标识>` | `.github/skills/code-review/SKILL.md` | 对一次代码改动做项目感知评审 |
~~~

## Constraints

- Only write `.github/copilot-instructions.md` unless the user explicitly asks for other edits.
- Base all facts on repository evidence or user answers.
- Do not invent frameworks, commands, branches, or conventions.
- Keep the skill portable; project-specific facts belong in `.github/copilot-instructions.md`, not in this skill.
