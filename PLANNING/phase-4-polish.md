# Phase 4: Polish & Austin Context

## Claude Code Prompt

```
claude --dangerously-skip-permissions
```

### Prompt:

Implement Phase 4: Polish & Austin Context for the Crowley Capital Diligence Tool.

## Objective

Integrate Austin market context, polish outputs, and finalize the system.

## Tasks

### 1. Austin Market Integration
Location: `skills/austin-market/scripts/`

Files to create:
- `valuation_context.py` — Compare deal to Austin benchmarks
- `investor_lookup.py` — Identify potential co-investors
- `acquirer_analysis.py` — Map potential acquirers

### 2. Enhanced Outputs
- Add Austin context to investment memos
- Include local investor suggestions
- Add exit potential based on local acquirers

### 3. Export Packaging
Location: `scripts/`

Files to create:
- `package_dataroom.py` — Create complete data room package

Features:
- Collect all outputs
- Generate table of contents
- Create ZIP archive
- Timestamp versioning

### 4. End-to-End Testing
- Test full workflow with sample company
- Verify all outputs generate correctly
- Check file organization

### 5. Documentation Polish
- Update CLAUDE.md with final commands
- Update QUICK-REFERENCE.md
- Add usage examples

## Success Criteria
- [ ] Austin context appears in outputs
- [ ] Export creates complete ZIP package
- [ ] End-to-end test passes
- [ ] Documentation is complete

## Completion
System ready for production use.
