# Crowley Capital Diligence Tool

**Internal VC Due Diligence Automation System**

A comprehensive Claude Code-powered tool for automating startup due diligence, built for Crowley Capital's Austin-focused investing.

---

## Overview

This tool transforms messy startup data into professional data room packages by automating:

- **SaaS Metrics Calculation** — LTV, CAC, NRR, churn, cohort analysis
- **Cap Table Modeling** — Dilution scenarios, waterfall analysis, round modeling
- **Risk Assessment** — Tunguz 11-risks framework scoring
- **Output Generation** — Investment memos, dashboards, partner meeting materials

## Quick Start

### 1. Initialize a Deal
```bash
/diligence init acme-corp
```

### 2. Upload Files
Place files in the appropriate directories:
- `./data-room/raw/financials/` — P&L, revenue data
- `./data-room/raw/customers/` — Customer lists, CRM exports
- `./data-room/raw/captable/` — Carta exports, cap table CSVs

### 3. Run Analysis
```bash
/diligence analyze --all
```

### 4. Generate Risk Assessment
```bash
/diligence risks
```

### 5. Export Data Room
```bash
/diligence export
```

## Commands

| Command | Description |
|---------|-------------|
| `/diligence init <company>` | Initialize new data room |
| `/diligence analyze --all` | Run all analysis subagents |
| `/diligence analyze --metrics` | Calculate SaaS metrics only |
| `/diligence captable --model` | Model proposed round |
| `/diligence risks` | Generate 11-risks scorecard |
| `/diligence export` | Package final data room |
| `/diligence compare <a> <b>` | Compare two deals |

## Skills

- **saas-metrics**: LTV, CAC, NRR, churn, cohorts
- **cap-table-modeling**: Dilution, waterfalls, round modeling
- **risk-framework**: Tunguz 11-risks scoring
- **data-room-templates**: Memos, dashboards, exports
- **austin-market**: Regional context

## Implementation Phases

| Phase | Description |
|-------|-------------|
| Phase 0 | Foundation Setup |
| Phase 1 | Core Skills (Metrics, Cap Table) |
| Phase 2 | Subagent Integration & Hooks |
| Phase 3 | Risk Assessment & Outputs |
| Phase 4 | Polish & Austin Context |

---

*Built by Jordaaan for Crowley Capital — Austin, TX*
