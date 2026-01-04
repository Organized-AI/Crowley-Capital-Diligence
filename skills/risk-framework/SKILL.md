---
name: risk-framework
description: Evaluates startup investments using the Tunguz 11-risks framework. Generates weighted scorecards with veto rules and investment recommendations. Use when assessing deal risks, preparing IC memos, or systematically evaluating a startup. Triggers on "risk assessment", "11 risks", "scorecard", "deal evaluation", "IC memo".
---

# Risk Assessment Skill (Tunguz Framework)

## Workflow

Copy this checklist:
```
Risk Assessment Progress:
- [ ] Step 1: Score each of the 11 risks (1-10)
- [ ] Step 2: Check veto rules (auto-pass conditions)
- [ ] Step 3: Calculate weighted score
- [ ] Step 4: Document key evidence for each score
- [ ] Step 5: Generate recommendation with mitigations
```

## The 11 Risks

| # | Risk | Question | Weight |
|---|------|----------|--------|
| 1 | Timing | Market ready now? | 5% |
| 2 | Business Model | Sustainable revenue? | 12% |
| 3 | Adoption | Customers buying? | 10% |
| 4 | Market Size | Big enough? | 12% |
| 5 | Execution | Team can ship/scale? | 10% |
| 6 | Technology | Defensible tech? | 8% |
| 7 | Capitalization | Runway sufficient? | 8% |
| 8 | Competition | Can they win? | 8% |
| 9 | Team | Right people? | 15% |
| 10 | Regulatory | Compliance risk? | 5% |
| 11 | Exit | Fund returner? | 7% |

## Scoring Guide

| Score | Definition |
|-------|------------|
| 9-10 | Clear strength/advantage |
| 7-8 | Above average, low risk |
| 5-6 | Acceptable, manageable |
| 3-4 | Concerning, needs mitigation |
| 1-2 | Critical, potential deal-breaker |

## Veto Rules (Auto-Pass)

- Team < 3
- Market Size < 4
- Business Model < 3
- **Any category = 1**

## Recommendation Thresholds

| Score | Recommendation |
|-------|----------------|
| 8.0+ | 🟢 Strong conviction — lead |
| 7.0-7.9 | 🟢 Positive — participate |
| 6.0-6.9 | 🟡 Cautious — mitigate risks |
| 5.0-5.9 | 🔴 Pass — monitor only |
| <5.0 | 🔴 Clear pass |

## Output Template

```markdown
## [Company] Risk Scorecard

| Risk | Score | Evidence |
|------|-------|----------|
| Team | X/10 | [Key finding] |
| Market Size | X/10 | [Key finding] |
...

**Weighted Score:** X.X/10
**Recommendation:** [Lead/Participate/Pass]
**Key Mitigations:** [If applicable]
```

## References

- [references/scoring-rubrics.md](references/scoring-rubrics.md) — Detailed criteria per risk
- [references/evidence-gathering.md](references/evidence-gathering.md) — Data sources per category
