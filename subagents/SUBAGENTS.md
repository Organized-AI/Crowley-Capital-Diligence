# Crowley Capital Diligence Subagents

## Architecture

Subagents are autonomous workers spawned for specific analysis tasks. They run in parallel and report back to the orchestrator.

## Subagent Definitions

### financial-analyst
- **Trigger:** `/diligence analyze --financials`
- **Inputs:** `./data-room/raw/financials/*`
- **Outputs:** `financial-model.xlsx`, `financial-summary.md`
- **Skills:** saas-metrics

### captable-modeler
- **Trigger:** `/diligence captable --model`
- **Inputs:** `./data-room/raw/captable/*`
- **Outputs:** `captable-model.xlsx`, `dilution-scenarios.md`
- **Skills:** cap-table-modeling

### metrics-engine
- **Trigger:** `/diligence analyze --metrics`
- **Inputs:** `./data-room/raw/revenue/*`, `./data-room/raw/customers/*`
- **Outputs:** `metrics-dashboard.html`, `metrics-summary.json`
- **Skills:** saas-metrics

### customer-analyzer
- **Trigger:** `/diligence analyze --customers`
- **Inputs:** `./data-room/raw/customers/*`
- **Outputs:** `customer-analysis.xlsx`, `reference-call-list.md`
- **Skills:** saas-metrics

### risk-assessor
- **Trigger:** `/diligence risks`
- **Inputs:** All analysis outputs + flags.md
- **Outputs:** `risk-scorecard.md`, `investment-memo.md`
- **Skills:** risk-framework, data-room-templates
- **Depends on:** All other subagents

## Parallel Execution

```
/diligence analyze --all
    │
    ├── [PARALLEL] financial-analyst
    ├── [PARALLEL] captable-modeler
    ├── [PARALLEL] metrics-engine
    └── [PARALLEL] customer-analyzer
             │
             ▼
        [AWAIT ALL]
             │
             ▼
        risk-assessor
```
