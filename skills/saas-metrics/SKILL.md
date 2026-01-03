---
name: saas-metrics
description: Calculate and benchmark SaaS/subscription business metrics for venture capital due diligence. Use when analyzing startup financials, calculating LTV/CAC/NRR/churn, building cohort analyses, evaluating unit economics, or benchmarking metrics against industry standards. Triggers on "calculate metrics", "unit economics", "LTV CAC", "churn analysis", "cohort retention", "SaaS benchmarks".
---

# SaaS Metrics Calculation Skill

Calculate, validate, and benchmark SaaS metrics for Crowley Capital due diligence.

## Quick Reference

| Metric | Formula | Good | Watch | Risk |
|--------|---------|------|-------|------|
| LTV | (ARPU × Gross Margin) / Monthly Churn | >$15k | $5-15k | <$5k |
| CAC | (Sales + Marketing) / New Customers | <LTV/3 | LTV/3-2 | >LTV/2 |
| LTV:CAC | LTV / CAC | >3.0 | 2.0-3.0 | <2.0 |
| Payback | CAC / (ARPU × Gross Margin) | <12mo | 12-18mo | >18mo |
| Gross Churn | Lost MRR / Starting MRR | <2% | 2-5% | >5% |
| NRR | (Start + Expansion - Churn) / Start | >110% | 100-110% | <100% |
| Burn Multiple | Net Burn / Net New ARR | <1.5 | 1.5-2.5 | >2.5 |
| Gross Margin | (Revenue - COGS) / Revenue | >70% | 60-70% | <60% |

## Workflow

1. **Ingest data** → Run `scripts/parse_revenue_data.py`
2. **Calculate metrics** → Run `scripts/calculate_metrics.py`
3. **Build cohorts** → Run `scripts/cohort_analysis.py`
4. **Benchmark** → Compare against `references/benchmarks.md`

## Scripts

| Script | Purpose |
|--------|---------|
| `calculate_metrics.py` | Calculate all core metrics |
| `cohort_analysis.py` | Build retention cohort matrix |

## References

- `references/benchmarks.md` — Benchmark tables by stage
- `references/formulas.md` — Detailed formula derivations
- `references/red-flags.md` — Manipulation tactics to detect
