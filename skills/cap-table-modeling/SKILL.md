---
name: cap-table-modeling
description: Models cap tables, dilution scenarios, and exit waterfalls for VC due diligence. Use when analyzing ownership structures, modeling investment rounds, calculating dilution, building waterfall analyses, or reviewing liquidation preferences. Triggers on "cap table", "dilution", "ownership", "waterfall", "liquidation preference", "option pool".
---

# Cap Table Modeling Skill

## Workflow

Copy this checklist:
```
Cap Table Analysis:
- [ ] Step 1: Parse cap table (run parse_captable.py)
- [ ] Step 2: Validate share counts match totals
- [ ] Step 3: Model proposed round (run model_round.py)
- [ ] Step 4: Build exit waterfall (run waterfall_analysis.py)
- [ ] Step 5: Check red flags and document findings
```

**Validation (Step 2)**: Sum all share classes. If total differs from stated fully-diluted count by >0.5%, flag data quality issue.

## Quick Reference

| Stage | Typical Dilution | Option Pool | Founder Target |
|-------|-----------------|-------------|----------------|
| Seed | 15-25% | 10-15% | >60% |
| Series A | 20-30% | 15-20% | >40% |
| Series B | 15-25% | 15-20% | >25% |
| Series C+ | 10-20% | 10-15% | >15% |

## Red Flags

| Flag | Threshold | Action |
|------|-----------|--------|
| Liquidation preference | >1.5x | Model downside scenarios |
| Participating preferred | Uncapped | Calculate break-even exit |
| Option pool shuffle | >25% pre-money | Flag in memo |
| Founder dilution | <10% pre-B | Assess motivation risk |
| Full ratchet anti-dilution | Any | Model down-round impact |

## Scripts

| Script | Input | Output |
|--------|-------|--------|
| `parse_captable.py` | Carta/CSV export | `parsed_captable.json` |
| `model_round.py` | Round terms + cap table | Dilution analysis |
| `waterfall_analysis.py` | Cap table + exit values | Payout scenarios |

## References

- [references/term-sheets.md](references/term-sheets.md) — Standard vs. aggressive terms
- [references/waterfall-examples.md](references/waterfall-examples.md) — Sample exit calculations
