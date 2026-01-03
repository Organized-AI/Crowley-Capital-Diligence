# System Architecture

## Overview

The Crowley Capital Diligence Tool uses a three-layer architecture:

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
│                    Claude Code Commands                         │
│         /diligence init | analyze | risks | export              │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                      ORCHESTRATION LAYER                        │
├─────────────────────────────────────────────────────────────────┤
│  SUBAGENTS (Parallel Workers)                                   │
│  ├── financial-analyst     → P&L parsing, burn, projections     │
│  ├── captable-modeler      → Dilution, waterfall analysis       │
│  ├── metrics-engine        → LTV, CAC, NRR, cohorts             │
│  ├── customer-analyzer     → Concentration, segments            │
│  └── risk-assessor         → 11-risks scoring, recommendations  │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                       KNOWLEDGE LAYER                           │
├─────────────────────────────────────────────────────────────────┤
│  SKILLS (Reusable Modules)                                      │
│  ├── saas-metrics          → Formulas, benchmarks, red-flags    │
│  ├── cap-table-modeling    → Round terms, preferences           │
│  ├── risk-framework        → 11-risks definitions, weights      │
│  ├── data-room-templates   → Memo/dashboard templates           │
│  ├── austin-market         → Regional context, investors        │
│  ├── data-audit            → Meta Ads analysis                  │
│  └── data-room             → Egnyte MCP integration             │
└────────────────────────────┬────────────────────────────────────┘
                             │
┌────────────────────────────▼────────────────────────────────────┐
│                       AUTOMATION LAYER                          │
├─────────────────────────────────────────────────────────────────┤
│  HOOKS (Event-Driven Triggers)                                  │
│  ├── on-file-upload        → Validate, categorize, log          │
│  ├── on-metric-threshold   → Flag violations                    │
│  ├── on-analysis-complete  → Trigger risk assessment            │
│  └── on-export             → Package deliverables               │
└─────────────────────────────────────────────────────────────────┘
```

## Data Flow

```
                    ┌─────────────────┐
                    │   User Upload   │
                    │  (CSV/XLSX/PDF) │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ on-file-upload  │
                    │   (validate)    │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
     ┌────────▼────┐  ┌──────▼──────┐ ┌─────▼─────┐
     │ financials/ │  │ customers/  │ │ captable/ │
     └────────┬────┘  └──────┬──────┘ └─────┬─────┘
              │              │              │
              └──────────────┼──────────────┘
                             │
                    ┌────────▼────────┐
                    │    SUBAGENTS    │
                    │   (parallel)    │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ on-metric-      │
                    │ threshold       │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ on-analysis-    │
                    │ complete        │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │ risk-assessor   │
                    │ (11-risks)      │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │   on-export     │
                    │ (package ZIP)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Final Package  │
                    │ (Data Room ZIP) │
                    └─────────────────┘
```

## External Integrations

### Egnyte MCP (Data Room)
- Secure document access
- AI-powered document analysis
- Knowledge base queries
- Contract review automation

### Pipeboard Meta MCP (Data Audit)
- Ad account performance analysis
- Campaign insights
- Attribution assessment

### Stape MCP (Data Audit)
- Server-side tracking setup
- CAPI implementation
- Container management

## File Outputs

| Output | Format | Purpose |
|--------|--------|---------|
| metrics-summary.json | JSON | Calculated metrics |
| financial-model.xlsx | XLSX | P&L with projections |
| captable-model.xlsx | XLSX | Pro forma cap table |
| waterfall.xlsx | XLSX | Exit scenarios |
| cohort-analysis.xlsx | XLSX | Retention matrices |
| metrics-dashboard.html | HTML | Interactive charts |
| risk-scorecard.md | MD | 11-risks assessment |
| investment-memo.md | MD | Partner meeting memo |
| key-questions.md | MD | Founder discussion |
