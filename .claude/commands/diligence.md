# /diligence Commands

## Available Commands

### /diligence init <company-name>
Creates a new diligence folder for a company.
- Creates `./data-room/<company>/` structure
- Initializes intake log and flags file
- Sets active company context

### /diligence ingest <file-path>
Processes an uploaded file.
- Validates file structure
- Categorizes (financials/customers/captable)
- Logs to intake log
- Suggests next analysis step

### /diligence analyze [options]
Runs analysis subagents.

Options:
- `--all` — Run all analyses in parallel
- `--financials` — Financial statement analysis only
- `--metrics` — SaaS metrics calculation only
- `--customers` — Customer analysis only

### /diligence captable [options]
Cap table operations.

Options:
- `--model` — Model proposed round
- `--waterfall` — Generate exit waterfall
- `--raise <amount>` — Raise amount
- `--pre <valuation>` — Pre-money valuation
- `--pool <percent>` — Target option pool

### /diligence risks
Generate 11-risks scorecard.
- Requires analysis to be complete
- Outputs risk-scorecard.md
- Outputs investment-memo.md
- Outputs key-questions.md

### /diligence export
Package final data room.
- Creates timestamped export folder
- Generates ZIP archive
- Copies to outputs for download

### /diligence compare <company-a> <company-b>
Side-by-side deal comparison.
- Compares key metrics
- Compares risk scores
- Generates comparison report
