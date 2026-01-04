---
name: business-fin-analyst
description: Analyzes financial CSV/Excel files for VC due diligence. Calculates revenue trends, burn rate, margins, and runway from P&L data. Use when processing financial statements, analyzing expense breakdowns, or validating financial data quality. Triggers on "analyze financials", "P&L analysis", "burn rate", "revenue breakdown", "financial model".
---

# Business Financial Analyst Skill

## Workflow

Copy this checklist:
```
Financial Analysis:
- [ ] Step 1: Load data (run analyze_financials.py --load)
- [ ] Step 2: Validate data quality
- [ ] Step 3: Calculate core metrics
- [ ] Step 4: Generate visualizations
- [ ] Step 5: Export summary report
```

## Quick Start

```bash
# Full analysis
python scripts/analyze_financials.py \
  --input data-room/raw/financials/p&l.xlsx \
  --output data-room/analysis/financial-summary.json

# Validation only
python scripts/analyze_financials.py --validate-only
```

## Supported Formats

| Format | Extensions |
|--------|------------|
| CSV | `.csv` |
| Excel | `.xlsx`, `.xls` |
| Google Sheets | Export to CSV first |

## Output Metrics

| Category | Metrics |
|----------|---------|
| Revenue | Total, monthly average, MoM growth |
| Burn | Net burn, runway months, status |
| Margins | Gross margin, operating margin |
| Quality | Null counts, anomaly flags |

## Data Quality Validation

The script automatically checks for:
- Null values in critical columns
- Negative revenue (flag as error)
- Date gaps > 35 days
- Column name normalization

## Common Questions Answered

| Question | Script Flag |
|----------|-------------|
| "What's the burn rate?" | `--analyze burn` |
| "Show revenue trend" | `--analyze revenue --chart` |
| "What are the margins?" | `--analyze margins` |
| "Any data issues?" | `--validate-only` |

## Integration

Works with **saas-metrics** skill:
1. Load raw financials here
2. Pass cleaned data to saas-metrics for LTV/CAC

Works with **data-room** skill:
1. Fetch documents from Egnyte
2. Process with this skill

## References

- [references/column-mapping.md](references/column-mapping.md) — Standard column names
- [references/analysis-functions.md](references/analysis-functions.md) — Function reference
- [scripts/analyze_financials.py](scripts/analyze_financials.py) — Main script

## Dependencies

```
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.14.0
openpyxl>=3.1.0
```
