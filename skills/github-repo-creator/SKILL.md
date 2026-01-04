---
name: github-repo-creator
description: Creates GitHub repositories via CLI using gh tool. Handles org/personal repos, visibility settings, and initial setup. Use when creating new repos, initializing projects on GitHub, or pushing new projects. Triggers on "create repo", "new repository", "set up GitHub repo", "make a repo".
---

# GitHub Repository Creator

## Workflow

Copy this checklist:
```
Repo Creation:
- [ ] Step 1: Verify gh CLI installed (gh auth status)
- [ ] Step 2: Gather requirements (name, org, visibility)
- [ ] Step 3: Create repository
- [ ] Step 4: Clone to project directory
- [ ] Step 5: Initialize with structure
```

## Quick Commands

```bash
# Check auth
gh auth status

# Create org repo
gh repo create organized-ai/<name> --public --description "desc"

# Create personal repo
gh repo create jhillbht/<name> --public

# Create from existing local project
gh repo create <name> --source=. --public --push

# Clone to standard location
cd "/path/to/projects" && gh repo clone <org>/<name>

# List repos / view in browser / delete
gh repo list organized-ai
gh repo view <repo> --web
gh repo delete <org>/<repo> --yes
```

## Common Flags

| Flag | Purpose |
|------|---------|
| `--public` / `--private` | Visibility |
| `--description "text"` | Description |
| `--license mit` | Add license |
| `--gitignore Node` | Add .gitignore |

## Accounts

| Type | URL |
|------|-----|
| Personal | github.com/jhillbht |
| Organization | github.com/organized-ai |

## Post-Creation

Offer to:
1. Initialize with README/.gitignore
2. Apply organized-codebase-applicator template
3. Open in editor
