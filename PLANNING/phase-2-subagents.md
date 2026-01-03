# Phase 2: Subagent Integration & Hooks

## Claude Code Prompt

```
claude --dangerously-skip-permissions
```

### Prompt:

Implement Phase 2: Subagent Integration & Hooks for the Crowley Capital Diligence Tool.

## Objective

Create the /diligence slash command, subagent prompt files, and automation hooks.

## Tasks

### 1. Create /diligence Slash Command
Location: `.claude/commands/diligence.md`

Subcommands:
- `init <company>` — Initialize new deal folder
- `analyze --all` — Run all analysis subagents
- `analyze --financials` — Run financial analysis
- `analyze --metrics` — Run metrics analysis
- `analyze --customers` — Run customer analysis
- `captable --model` — Run cap table modeling
- `risks` — Generate risk scorecard
- `export` — Package data room

### 2. Create Subagent Prompt Files
Location: `.claude/agents/prompts/`

Files to create:
- `financial-analyst.md`
- `captable-modeler.md`
- `metrics-engine.md`
- `customer-analyzer.md`
- `risk-assessor.md`

### 3. Implement Hooks
Location: `.claude/hooks/scripts/`

Scripts to create:
- `validate-upload.py` — Validate uploaded files
- `check-thresholds.py` — Check metric thresholds
- `package-export.py` — Package data room for export

### 4. Create Hook Configuration
Location: `.claude/settings.json` or hook config

## Success Criteria
- [ ] /diligence command responds to all subcommands
- [ ] Subagent prompts correctly invoke skills
- [ ] Hooks trigger on appropriate events
- [ ] Integration test passes with sample data

## Next Phase
Phase 3: Risk Assessment & Outputs
