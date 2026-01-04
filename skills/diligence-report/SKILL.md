---
name: diligence-report
description: Generates professional PDF reports for VC due diligence. Compiles metrics, cap table, risk assessment, and market context into executive-ready documents with Mermaid visualizations. Use when finalizing diligence, creating IC materials, or generating LP reports. Triggers on "generate report", "create PDF", "IC materials", "diligence report".
---

# Diligence Report Generator

## Workflow

Copy this checklist:
```
Report Generation:
- [ ] Step 1: Verify source files exist
- [ ] Step 2: Generate Mermaid charts (MCP)
- [ ] Step 3: Build PDF (run generate_report.py)
- [ ] Step 4: Validate output opens correctly
- [ ] Step 5: Export to data-room/output/
```

## Source Files Required

```python
SOURCE_FILES = {
    "metrics": "data-room/analysis/metrics.json",
    "cap_table": "data-room/analysis/parsed_captable.json",
    "risk_scorecard": "data-room/output/risk-scorecard.md",
    "investment_memo": "data-room/output/investment-memo.md",
}
```

**Validation (Step 1)**: Check each file exists. If missing, run the prerequisite skill first.

## Generate PDF

```bash
python scripts/generate_report.py \
  --company "Company Name" \
  --data-room ./data-room \
  --output ./data-room/output/diligence-report.pdf \
  --format executive
```

**Options:**
- `--format executive` — 8-10 pages (default)
- `--format detailed` — 20+ pages
- `--format ic` — IC materials format
- `--include-appendix` — Add raw data

## Integration

| Skill | Data Provided |
|-------|---------------|
| saas-metrics | metrics.json, cohorts |
| cap-table-modeling | parsed_captable.json, waterfall |
| risk-framework | risk-scorecard.md |
| austin-market | Comparable valuations |
| carta-integration | Real-time cap table |

## References

- [references/report-structure.md](references/report-structure.md) — Page layouts and templates
- [references/mermaid-templates.md](references/mermaid-templates.md) — Chart code snippets
- [references/style-guide.md](references/style-guide.md) — Crowley Capital branding
- [scripts/generate_report.py](scripts/generate_report.py) — Main generator
- [scripts/mermaid_charts.py](scripts/mermaid_charts.py) — Chart utilities

## Dependencies

```
reportlab>=4.0.0
pypdf>=3.0.0
Pillow>=9.0.0
pandas>=2.0.0
```
