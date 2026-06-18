# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal technology blog/knowledge base written entirely in Markdown. It serves as a wiki rendered from a Git repo.

## Structure

- Each topic area has its own directory: `Git/`, `Golang/`, `Linux/`, `PHP/`
- `README.md` is the sole index/table of contents for all documents
- `uploads/` contains images referenced by blog posts

## Conventions

### File Naming

- All filenames use **English kebab-case** with the format: `topic-purpose.md`
- Examples: `gitlab-docker-deployment.md`, `git-multiple-ssh-keys.md`, `postfix-mail-server-setup.md`

### Adding New Posts

1. Create the markdown file in the appropriate topic directory
2. Add a corresponding entry in `README.md` (table format with Title and Description columns)

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
