# Crowley Capital Diligence Hooks

## Hook Architecture

Hooks are event-triggered actions that fire automatically when specific conditions are met.

## Hook Definitions

### on-file-upload
- **Trigger:** File added to `./data-room/raw/`
- **Actions:**
  - Detect file type (CSV, XLSX, PDF)
  - Validate structure
  - Auto-categorize (financials, customers, captable)
  - Log to `./data-room/intake-log.md`
  - Suggest next command

### on-metric-threshold
- **Trigger:** metrics-engine completes
- **Actions:**
  - Compare metrics against thresholds
  - Auto-flag violations to `./data-room/flags.md`

**Thresholds:**
| Metric | Red | Yellow |
|--------|-----|--------|
| LTV:CAC | <2.0 | <3.0 |
| Gross Churn | >5% | >2% |
| NRR | <100% | <110% |
| Burn Multiple | >2.5 | >1.5 |
| Runway | <12mo | <18mo |

### on-analysis-complete
- **Trigger:** All analysis subagents complete
- **Actions:**
  - Verify all outputs exist
  - Create `.analysis-complete` signal
  - Trigger risk-assessor

### on-export
- **Trigger:** `/diligence export`
- **Actions:**
  - Package all outputs
  - Create timestamped folder
  - Generate ZIP archive
  - Copy to outputs for download
