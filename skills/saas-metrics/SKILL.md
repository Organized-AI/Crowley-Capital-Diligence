---
name: saas-metrics
description: Calculates and benchmarks SaaS metrics (LTV, CAC, NRR, churn, cohorts) for VC due diligence. Use when analyzing startup financials, evaluating unit economics, building cohort analyses, or benchmarking against industry standards. Triggers on "calculate metrics", "unit economics", "LTV CAC", "churn analysis", "cohort", "SaaS benchmarks".
---

# SaaS Metrics Skill

## Quick Reference

| Metric | Formula | 🟢 Good | 🟡 Watch | 🔴 Risk |
|--------|---------|---------|----------|---------|
| LTV | (ARPU × GM) / Monthly Churn | >$15k | $5-15k | <$5k |
| CAC | (S&M Spend) / New Customers | <LTV/3 | LTV/3-2 | >LTV/2 |
| LTV:CAC | LTV / CAC | >3.0 | 2.0-3.0 | <2.0 |
| Payback | CAC / (ARPU × GM) | <12mo | 12-18mo | >18mo |
| Gross Churn | Lost MRR / Start MRR | <2% | 2-5% | >5% |
| NRR | (Start + Expand - Churn) / Start | >110% | 100-110% | <100% |
| Burn Multiple | Net Burn / Net New ARR | <1.5 | 1.5-2.5 | >2.5 |
| Gross Margin | (Rev - COGS) / Rev | >70% | 60-70% | <60% |

## Workflow

Copy this checklist:
```
SaaS Metrics Progress:
- [ ] Step 1: Parse revenue data (run parse_revenue_data.py)
- [ ] Step 2: Calculate core metrics (run calculate_metrics.py)
- [ ] Step 3: Validate outputs against benchmarks
- [ ] Step 4: Build cohort matrix (run cohort_analysis.py)
- [ ] Step 5: Flag anomalies and document findings
```

**Step 3 validation**: Compare results against [references/benchmarks.md](references/benchmarks.md). Flag any metric 2+ tiers below stage median.

## Red Flags to Detect

See [references/red-flags.md](references/red-flags.md) for manipulation tactics:
- Cohort windows starting mid-month
- One-time revenue in MRR
- Implementation fees in ARR
- Logo churn hiding MRR churn

## References

- [references/benchmarks.md](references/benchmarks.md) — Thresholds by stage (Seed → Series C)
- [references/formulas.md](references/formulas.md) — Detailed derivations
- [references/red-flags.md](references/red-flags.md) — Manipulation patterns
