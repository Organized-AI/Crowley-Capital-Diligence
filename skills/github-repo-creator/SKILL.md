---
name: github-repo-creator
description: Create GitHub repositories directly from CLI without visiting github.com. Use when user wants to create a new repo, initialize a project on GitHub, set up a new repository, or push a new project to GitHub. Triggers include "create repo", "new repository", "set up GitHub repo", "initialize GitHub project", "make a repo", or any request to create/setup a GitHub repository.
---

# GitHub Repository Creator

Create and configure GitHub repositories via CLI using the `gh` GitHub CLI tool.

## Prerequisites Check

1. Identify which machine is being used:
   - `users/supabowl` = MacBook M1 Pro
   - `users/jordaaan` = M4 Mac Mini

2. Verify `gh` CLI installation and authentication:
```bash
gh --version && gh auth status
```

If not installed: `brew install gh && gh auth login`

## Repository Creation Workflow

### Step 1: Gather Requirements

Ask user for:
- **Repository name** (kebab-case recommended)
- **Organization**: Personal (`jhillbht`) or Organization (`organized-ai`)
- **Visibility**: Public or Private (default: public)

### Step 2: Create Repository

```bash
# For organization repo
gh repo create organized-ai/<repo-name> --public --description "<description>"

# For personal repo
gh repo create jhillbht/<repo-name> --public --description "<description>"
```

**Common flags:**
- `--public` / `--private` - visibility
- `--description "text"` - repo description
- `--license mit` - add license
- `--gitignore Node` - add .gitignore template

### Step 3: Clone to Default Directory

Clone to the standard project location:

```bash
cd "/Users/supabowl/Library/Mobile Documents/com~apple~CloudDocs/BHT Promo iCloud/Organized AI/Windsurf"
gh repo clone <org>/<repo-name>
```

### Step 4: Offer Next Steps

After creation, offer to:
1. Initialize with README, .gitignore, starter structure
2. Apply Organized Codebase template (use organized-codebase-applicator skill)
3. Open in Cursor/VS Code

## Quick Reference Commands

```bash
# Create + clone in one step (from existing local project)
gh repo create <name> --source=. --public --push

# List repos in org
gh repo list organized-ai

# View repo in browser
gh repo view <repo> --web

# Delete repo (use with caution)
gh repo delete <org>/<repo> --yes
```

## GitHub Accounts Reference

- **Personal**: `https://github.com/jhillbht`
- **Organization**: `https://github.com/organized-ai`
