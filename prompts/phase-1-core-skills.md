# Phase 1: Core Skills Implementation

## Claude Code Prompt

```
claude --dangerously-skip-permissions
```

### Prompt:

Implement Phase 1: Core Skills for the Crowley Capital Diligence Tool.

## Objective

Implement Python scripts for saas-metrics and cap-table-modeling skills.

## Tasks

### 1. saas-metrics Scripts
- `calculate_metrics.py` — Full metrics calculator
- `cohort_analysis.py` — Retention cohort builder

### 2. cap-table-modeling Scripts  
- `parse_captable.py` — Parse Carta/CSV exports
- `model_round.py` — Model new rounds
- `waterfall_analysis.py` — Exit waterfalls

### 3. Test with Sample Data
```bash
python skills/saas-metrics/scripts/calculate_metrics.py \
  --revenue test-data/sample-revenue.csv \
  --customers test-data/sample-customers.csv \
  --output data-room/analysis/metrics.json
```

## Success Criteria
- [ ] calculate_metrics.py produces accurate metrics
- [ ] cohort_analysis.py generates retention matrices
- [ ] Cap table scripts handle standard formats
- [ ] All tests pass with sample data

## Next Phase
Phase 2: Subagent Integration
