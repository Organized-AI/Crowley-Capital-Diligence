---
name: cap-table-modeling
description: Model cap tables, dilution scenarios, and exit waterfalls for venture capital due diligence. Use when analyzing startup ownership structures, modeling investment rounds, calculating founder/investor dilution, building exit scenario analyses, or understanding liquidation preferences. Triggers on "cap table", "dilution", "ownership", "waterfall analysis", "liquidation preference", "option pool".
---

# Cap Table Modeling Skill

Model ownership structures, dilution scenarios, and exit waterfalls.

## Key Concepts

| Term | Definition |
|------|------------|
| Pre-money | Company valuation before new investment |
| Post-money | Pre-money + new investment amount |
| Dilution | Reduction in ownership % from new shares |
| Option Pool | Shares reserved for employee equity |
| Liquidation Preference | Amount investors get paid first in exit |

## Standard Round Terms

| Term | Founder-Friendly | Standard | Investor-Favorable |
|------|------------------|----------|-------------------|
| Liquidation Pref | 1x non-participating | 1x participating (capped) | >1x participating |
| Option Pool | Post-money | Pre-money (15-20%) | Pre-money (>20%) |

## Typical Dilution by Stage

| Stage | Typical Dilution |
|-------|-----------------|
| Seed | 15-25% |
| Series A | 20-30% |
| Series B | 15-25% |
| Series C+ | 10-20% |

## Scripts

| Script | Purpose |
|--------|---------|
| `parse_captable.py` | Parse Carta/CSV exports |
| `model_round.py` | Model new investment round |
| `waterfall_analysis.py` | Build exit waterfall |

## Red Flags

| Red Flag | Why It Matters |
|----------|---------------|
| >2x liquidation preference | Returns to common severely impacted |
| Full ratchet anti-dilution | Founders crushed in down-round |
| >25% option pool pre-money | Excessive dilution to founders |
| Founder ownership <10% pre-Series B | May lack motivation |
