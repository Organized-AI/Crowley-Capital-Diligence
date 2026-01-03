# Phase 0: Project Foundation

## Claude Code Implementation Prompt

```
claude --dangerously-skip-permissions
```

### Prompt:

You are setting up the Crowley Capital Diligence Tool. This is Phase 0: Foundation Setup.

## Objective

Create the complete project structure, install dependencies, and set up base configuration.

## Tasks

### 1. Verify Project Structure
```
crowley-capital-diligence/
├── .claude/
├── skills/
│   ├── saas-metrics/
│   ├── cap-table-modeling/
│   ├── risk-framework/
│   ├── data-room-templates/
│   └── austin-market/
├── subagents/
├── hooks/
├── prompts/
├── data-room/
│   ├── raw/{financials,customers,captable,crm}
│   ├── analysis/
│   └── output/
└── test-data/
```

### 2. Create requirements.txt
```
pandas>=2.0.0
numpy>=1.24.0
openpyxl>=3.1.0
xlsxwriter>=3.1.0
matplotlib>=3.7.0
plotly>=5.14.0
jinja2>=3.1.0
pyyaml>=6.0
tabulate>=0.9.0
```

### 3. Create Test Data Files
Create sample CSV files in test-data/ for testing.

### 4. Initialize Git
```bash
git init
git add .
git commit -m "Phase 0: Project foundation"
```

## Success Criteria
- [ ] Directory structure created
- [ ] Dependencies installed
- [ ] Test data available
- [ ] Git initialized

## Next Phase
Phase 1: Core Skills Implementation
