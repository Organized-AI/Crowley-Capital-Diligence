# Phase 3: Risk Assessment & Outputs

## Claude Code Prompt

```
claude --dangerously-skip-permissions
```

### Prompt:

Implement Phase 3: Risk Assessment & Outputs for the Crowley Capital Diligence Tool.

## Objective

Create risk assessment tools and professional output generators.

## Tasks

### 1. Risk Scorecard Generator
Location: `skills/risk-framework/scripts/`

Files to create:
- `generate_scorecard.py` — Generate 11-risks scorecard from analysis
- `calculate_weighted_score.py` — Calculate weighted overall score

Features:
- Read all analysis outputs
- Apply 11-risks framework
- Calculate weighted scores
- Generate markdown scorecard
- Apply veto rules

### 2. Investment Memo Generator
Location: `skills/data-room-templates/scripts/`

Files to create:
- `generate_memo.py` — Generate investment memo
- `generate_summary.py` — Generate executive summary

### 3. Metrics Dashboard Generator
Location: `skills/data-room-templates/scripts/`

Files to create:
- `generate_dashboard.py` — Generate HTML metrics dashboard

Features:
- Interactive Plotly charts
- Key metrics summary
- Trend visualization
- Benchmark comparisons

### 4. Template Assets
Location: `skills/data-room-templates/assets/`

Files to create:
- `memo-template.md`
- `summary-template.md`
- `dashboard-template.html`

## Success Criteria
- [ ] Risk scorecard generates correctly from analysis
- [ ] Investment memo populates all sections
- [ ] Dashboard displays interactive charts
- [ ] Templates are professional quality

## Next Phase
Phase 4: Polish & Austin Context
