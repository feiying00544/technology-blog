---
allowed-tools: Bash(git add:*), Bash(git status:*), Bash(git commit:*), Bash(git diff:*), Bash(git log:*), Read
description: Stage and commit changes following the project's commit convention (auto-detects from CLAUDE.md)
---

## Context

- Git status: !`git status`
- Staged and unstaged diff: !`git diff HEAD`
- Recent commits (style reference): !`git log --oneline -5`

## Your Task

1. Read the current project's CLAUDE.md — locate the "Git Commit" or "Commit" convention section to determine the required commit message format.
2. If no CLAUDE.md exists or no commit convention section is found, use Conventional Commits as fallback: `type(scope): description`

### Determine Action/Type

Analyze the diff to infer the appropriate action:

| Condition | Action |
|-----------|--------|
| All changed files are newly created | Add / feat |
| All changed files are deleted | Remove |
| Diff fixes broken logic, incorrect conditions, typo corrections, error handling gaps | Fix |
| All other modifications (refactors, updates, enhancements) | Modify / refactor |

### Determine Module/Scope

- Derive from the directories or functional domains of changed files
- Use directory names as module names (e.g., `AI/` → AI, `Git/` → Git)
- For config/dotfiles changes: use `Config`
- For README-only changes: use `README`
- Multiple modules: comma-separated in one bracket pair, limit to 3-4 max

### Confirm Before Committing

Before staging and committing, present the user with:

1. **Files to stage** — list each file path you plan to `git add`
2. **Files excluded** — list modified/untracked files you will NOT include (and why)
3. **Proposed commit message** — the full message you will use

If the user provided a filter (e.g., "only md files", "only AI/ directory"), apply it strictly and show what was filtered out.

Wait for user confirmation before proceeding. If the user says to adjust, revise and re-present.

### Execute (after confirmation)

1. Stage ONLY the confirmed files with `git add <file>` (never use `git add .` or `git add -A`)
2. Create the commit with the confirmed message
3. NEVER include `Co-Authored-By` or any co-author attribution trailer
4. Maximum 4 lines for the entire commit message (subject + optional body)
