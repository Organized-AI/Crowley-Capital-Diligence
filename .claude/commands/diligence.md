# Crowley Capital Diligence Command

You are the Crowley Capital Diligence orchestrator. Parse the user's command and execute the appropriate workflow.

## Command: $ARGUMENTS

Parse the arguments and execute:

### `init <company>`
Initialize a new deal:
1. Create folder structure: `data-room/deals/<company>/`
2. Create subfolders: `raw/`, `analysis/`, `output/`
3. Create `deal-info.json` with company name and date
4. Log to intake-log.md
5. Respond: "Deal initialized for <company>. Upload files to data-room/deals/<company>/raw/"

### `analyze --all`
Run all analysis subagents in parallel:
1. Check for files in `data-room/raw/` or current deal folder
2. Run these analyses:
   - Financial analysis (if financials exist)
   - Metrics analysis (if revenue/customer data exists)
   - Customer analysis (if customer data exists)
   - Cap table analysis (if cap table exists)
3. Aggregate results to `data-room/analysis/`
4. Check metric thresholds and flag violations
5. Respond with summary of completed analyses

### `analyze --financials`
Run financial analysis:
1. Find financial files in `data-room/raw/financials/`
2. Use `skills/business-fin-analyst/scripts/analyze_financials.py`
3. Output to `data-room/analysis/financial-summary.json`

### `analyze --metrics`
Run SaaS metrics analysis:
1. Find revenue/customer files
2. Use `skills/saas-metrics/scripts/calculate_metrics.py`
3. Use `skills/saas-metrics/scripts/cohort_analysis.py`
4. Output to `data-room/analysis/`

### `analyze --customers`
Run customer analysis:
1. Find customer files
2. Analyze concentration, segments, churn
3. Generate reference call list
4. Output to `data-room/analysis/`

### `captable --model`
Run cap table modeling:
1. Find cap table files in `data-room/raw/captable/`
2. Use `skills/cap-table-modeling/scripts/parse_captable.py`
3. Ask user for round parameters if modeling new round
4. Use `skills/cap-table-modeling/scripts/model_round.py`
5. Use `skills/cap-table-modeling/scripts/waterfall_analysis.py`
6. Output to `data-room/analysis/`

### `risks`
Generate risk assessment:
1. Gather all analysis outputs
2. Use `skills/risk-framework/scripts/generate_scorecard.py`
3. Apply 11-risks framework with weights
4. Check veto rules
5. Generate recommendation
6. Output `risk-scorecard.md` to `data-room/output/`

### `export`
Package data room:
1. Collect all outputs from `data-room/analysis/` and `data-room/output/`
2. Generate table of contents
3. Create timestamped ZIP archive
4. Save to `data-room/exports/`
5. Respond with export location

### `compare <deal1> <deal2>`
Compare two deals:
1. Load metrics from both deals
2. Generate side-by-side comparison
3. Highlight key differences

## Error Handling
- If required files don't exist, prompt user to upload them
- If analysis fails, report specific error
- Always log actions to intake-log.md
