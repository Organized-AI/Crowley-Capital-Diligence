---
name: contract-review
description: Comprehensive contract review and analysis for VC due diligence. Covers term sheets, customer agreements, vendor contracts, employment agreements, IP assignments, and corporate documents. Use when reviewing legal documents for deals, identifying red flags, extracting key terms, or preparing negotiation points. Triggers on "review contract", "term sheet analysis", "red flags in agreement", "contract summary", "legal diligence".
---

# Contract Review Skill

Systematic contract analysis for VC due diligence at Crowley Capital.

## Document Types

### Investment Documents
- **Term Sheets** — Valuation, liquidation preferences, board seats, protective provisions
- **Stock Purchase Agreements** — Reps & warranties, closing conditions
- **Investor Rights Agreements** — Information rights, registration rights, ROFR
- **Voting Agreements** — Board composition, drag-along, tag-along

### Commercial Contracts
- **Customer Agreements** — SaaS terms, pricing, SLAs, liability caps
- **Vendor Contracts** — Critical dependencies, lock-in terms
- **Partnership Agreements** — Revenue shares, exclusivity, termination

### Corporate Documents
- **Employment Agreements** — Key person terms, non-competes, IP assignment
- **Founder Agreements** — Vesting, roles, buyback rights
- **IP Assignments** — Clean assignment of all relevant IP

## Review Workflow

### Phase 1: Document Intake

1. **Categorize Document Type**
   - Investment vs Commercial vs Corporate
   - Standard template vs heavily negotiated

2. **Extract Key Metadata**
   - Parties involved
   - Effective date
   - Term length
   - Governing law

### Phase 2: Key Terms Extraction

**For Term Sheets:**
```markdown
| Term | Value | Market Standard | Flag |
|------|-------|-----------------|------|
| Pre-money valuation | $X | [Seed/A benchmark] | 🟢/🟡/🔴 |
| Liquidation preference | 1x non-participating | 1x NP standard | 🟢 |
| Option pool | 15% post | 10-15% typical | 🟢 |
| Board composition | 2 founders, 1 investor | Balanced | 🟢 |
| Anti-dilution | Broad-based weighted avg | Standard | 🟢 |
| Protective provisions | Standard | [check list] | 🟢/🔴 |
| Drag-along | Majority approval | Standard | 🟢 |
```

**For Customer Agreements:**
```markdown
| Term | Value | Risk Level |
|------|-------|------------|
| Contract value | $X ARR | — |
| Term length | X years | — |
| Auto-renewal | Yes/No | — |
| Termination notice | X days | — |
| Termination for convenience | Yes/No | 🟢/🔴 |
| Liability cap | $X / X months fees | 🟢/🟡/🔴 |
| SLA uptime | 99.X% | — |
| SLA credits | X% | — |
```

### Phase 3: Red Flag Detection

**Investment Red Flags (Veto-Level):**
- [ ] Participating preferred (>1x participation cap)
- [ ] Full ratchet anti-dilution
- [ ] Founder vesting reset without acceleration
- [ ] Unusual protective provisions (hiring, spending)
- [ ] Pay-to-play with automatic conversion
- [ ] Unlimited board expansion rights
- [ ] Unreasonable drag-along threshold (<60%)

**Commercial Red Flags:**
- [ ] Customer concentration (>25% from one customer)
- [ ] Short-term contracts with easy termination
- [ ] Unlimited liability exposure
- [ ] MFN clauses that limit pricing
- [ ] Exclusivity that blocks expansion
- [ ] Auto-renewal without price caps

**Corporate Red Flags:**
- [ ] Missing IP assignments from founders/contractors
- [ ] Founder vesting complete (no remaining incentive)
- [ ] Key person without non-compete
- [ ] Pending or threatened litigation
- [ ] Outstanding option grants exceeding pool

### Phase 4: Summary Generation

**Executive Summary Format:**
```markdown
## Contract Summary: [Document Name]

**Type:** [Term Sheet / Customer Agreement / etc.]
**Parties:** [Company] ↔ [Counterparty]
**Value:** [$X] | **Term:** [X years]

### Key Terms
[3-5 most important terms]

### Red Flags
🔴 **Critical:** [Any veto-level issues]
🟡 **Notable:** [Items requiring attention]

### Negotiation Points
1. [Suggested change and rationale]
2. [Suggested change and rationale]

### Risk Assessment
| Category | Score | Notes |
|----------|-------|-------|
| Financial | X/5 | [reason] |
| Operational | X/5 | [reason] |
| Legal | X/5 | [reason] |
| **Overall** | **X/5** | |
```

## Standard Benchmarks

### Term Sheet Standards (Seed/Series A)

| Term | Seed Standard | Series A Standard |
|------|---------------|-------------------|
| Liquidation Pref | 1x non-participating | 1x non-participating |
| Anti-dilution | Broad-based weighted avg | Broad-based weighted avg |
| Option Pool | 10-15% post-money | 10-15% refreshed |
| Board Seats | 1 investor / 2 founder | 2 investor / 2 founder / 1 independent |
| Protective Provisions | Light (5-7 items) | Standard (10-12 items) |
| Information Rights | Quarterly financials | Monthly financials + annual audit |
| Pro-rata Rights | All investors | Lead + major investors |
| Vesting | 4 yr / 1 yr cliff | 4 yr / 1 yr cliff (may reset) |

### Customer Agreement Standards (Enterprise SaaS)

| Term | Market Standard | Red Flag Threshold |
|------|-----------------|-------------------|
| Contract Term | 12-36 months | <12 months |
| Termination Notice | 30-90 days | <30 days |
| Liability Cap | 12 months fees | Unlimited or >24 months |
| Termination for Convenience | No or with penalty | Yes, without penalty |
| Auto-renewal | Yes | No |
| Price Increase Cap | 5-10% annual | >15% or unlimited |

## Integration with Data Room

### Document Flow
```
Egnyte Data Room → Contract Review → Risk Scorecard
       ↓                   ↓                ↓
  Legal/Contracts/    Extract Terms    risk-framework
```

### Extraction Prompts (for Egnyte)

Use with data-room skill:
```python
# Term Sheet
ask_document(file_id, "What is the pre-money valuation?")
ask_document(file_id, "What are the liquidation preferences?")
ask_document(file_id, "What protective provisions are included?")

# Customer Agreement
ask_document(file_id, "What is the contract term and renewal?")
ask_document(file_id, "What is the liability cap?")
ask_document(file_id, "What are the termination conditions?")
```

## References

- `references/term-sheet-checklist.md` — Complete term sheet review checklist
- `references/red-flag-catalog.md` — Comprehensive red flag database
- `references/negotiation-playbook.md` — Common negotiation positions
- `references/standard-clauses.md` — Market standard language
