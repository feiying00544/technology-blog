# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal technology blog/knowledge base written entirely in Markdown. It serves as a wiki rendered from a Git repo.

## Structure

- Each topic area has its own directory: `AI/`, `Git/`, `Golang/`, `Linux/`, `PHP/`
- `README.md` is the sole index/table of contents for all documents
- `uploads/` contains images referenced by blog posts

## Conventions

### File Naming

- All filenames use **English kebab-case** with the format: `topic-purpose.md`
- Examples: `gitlab-docker-deployment.md`, `git-multiple-ssh-keys.md`, `postfix-mail-server-setup.md`

### Adding New Posts

1. Create the markdown file in the appropriate topic directory
2. Add a corresponding entry in `README.md` (table format with Title and Description columns)

### Git Commit 规范

- 提交说明（commit message）**不超过 4 行**。
- **禁止**包含 `Co-Authored-By` 行（或任何协作者署名）。

### Document Format

Each blog post should follow this structure:

1. H1 title (English, descriptive)
2. One-line summary
3. `---` separator
4. Structured sections with H2 headings
5. Code blocks with language hints (e.g., ```bash, ```yaml, ```ruby)
6. Use tables for structured comparisons
7. Use blockquotes (`>`) for important notes

### Image Assets

Images go in `uploads/` and are referenced by their hash-based filenames.

## Mermaid Diagrams

When a document benefits from a flowchart or diagram, use Mermaid syntax. All Mermaid diagrams must follow these rules for cross-platform compatibility:

**Compatibility targets:** Obsidian, GitHub Markdown, VS Code Markdown Preview.

**Rules:**
- Never use `\n` for line breaks inside node labels
- Use `<br>` instead for multi-line labels
- Avoid Mermaid experimental syntax
- Wrap diagrams in standard fenced code blocks: ` ```mermaid `

## 文档整理规则（可复用清单）

每次执行"整理/新增文档"任务时，直接照以下步骤做即可复用：

1. **选目录与文件名**：放入合适的主题目录（`AI/`、`Git/`、`Golang/`、`Linux/`、`PHP/`），文件名用英文 kebab-case，格式 `topic-purpose.md`。
2. **文档骨架**：H1 标题（英文、描述性）→ 一行摘要 → `---` 分隔线 → H2 分节；必要时摘要下加多行 blockquote 补充背景。
3. **语言约定**：正文语言依内容而定（教程类常用中文，运维类常用英文）；**代码/配置片段、frontmatter 字段名、文件名、CLI 命令一律保持英文原样**；**README 索引条目固定用英文**。
4. **表达元素**：结构化对比用表格；重要提示用 blockquote（`>`）；代码块必须带语言标识（```bash / ```yaml / ```json / ```toml / ```mermaid 等）。
5. **流程图**：需要时用 Mermaid，遵守上文「Mermaid Diagrams」规则（`<br>` 换行、禁实验语法、标准 ```mermaid 代码块）。
6. **时效与诚信**：涉及版本/特性/价格等时效性内容，必须核查官方源，并在文末标注「知识截止 YYYY-MM-DD」；无法核实的点显式标注「未核实」，**不臆造**。
7. **更新索引**：完成后在 `README.md` 对应分节（无则新建 `## 主题`，沿用两列 `Title | Description` 表格、英文条目）补上链接。
