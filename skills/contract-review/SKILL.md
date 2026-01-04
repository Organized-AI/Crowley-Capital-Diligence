---
name: contract-review
description: Reviews contracts for VC due diligence including term sheets, customer agreements, vendor contracts, and corporate documents. Extracts key terms, identifies red flags, and generates summaries with negotiation points. Use when reviewing legal documents, analyzing deal terms, or conducting legal diligence. Triggers on "review contract", "term sheet analysis", "red flags", "contract summary", "legal diligence".
---

# Contract Review Skill

## Workflow

Copy this checklist:
```
Contract Review:
- [ ] Step 1: Categorize document type
- [ ] Step 2: Extract key terms to table
- [ ] Step 3: Check against red flag checklist
- [ ] Step 4: Compare to market standards
- [ ] Step 5: Generate summary with negotiation points
```

## Document Types

| Category | Documents |
|----------|-----------|
| Investment | Term sheets, SPAs, IRA, Voting agreements |
| Commercial | Customer agreements, Vendor contracts, Partnerships |
| Corporate | Employment, Founder agreements, IP assignments |

## Term Extraction Templates

**Term Sheet:**
```markdown
| Term | Value | Standard | Flag |
|------|-------|----------|------|
| Pre-money | $X | [benchmark] | 🟢/🔴 |
| Liquidation pref | X | 1x NP | 🟢/🔴 |
| Anti-dilution | X | Broad-based | 🟢/🔴 |
| Option pool | X% | 10-15% | 🟢/🔴 |
| Board seats | X/X | Balanced | 🟢/🔴 |
```

**Customer Agreement:**
```markdown
| Term | Value | Risk |
|------|-------|------|
| Contract value | $X ARR | — |
| Term length | X years | 🟢/🔴 |
| Liability cap | $X | 🟢/🔴 |
| Termination | X days | 🟢/🔴 |
```

## Red Flags (Veto-Level)

### Investment
- [ ] Participating preferred (uncapped)
- [ ] Full ratchet anti-dilution
- [ ] Founder vesting reset
- [ ] Unusual protective provisions
- [ ] Unreasonable drag-along (<60%)

### Commercial
- [ ] Customer concentration >25%
- [ ] Short contracts + easy termination
- [ ] Unlimited liability
- [ ] Exclusivity blocking expansion

### Corporate
- [ ] Missing IP assignments
- [ ] Key person without non-compete
- [ ] Pending litigation

## Summary Template

```markdown
## Contract Summary: [Document Name]

**Type:** [Category] | **Parties:** [X] ↔ [Y] | **Value:** $X

### Key Terms
[3-5 most important]

### Red Flags
🔴 **Critical:** [Veto-level issues]
🟡 **Notable:** [Items needing attention]

### Negotiation Points
1. [Change + rationale]
2. [Change + rationale]

### Risk Score: X/5
```

## References

- [references/term-sheet-checklist.md](references/term-sheet-checklist.md) — Full checklist
- [references/red-flag-catalog.md](references/red-flag-catalog.md) — Comprehensive flags
- [references/market-standards.md](references/market-standards.md) — Benchmark terms
