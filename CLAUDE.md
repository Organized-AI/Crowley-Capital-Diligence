# Crowley Capital Diligence Tool

## Project Overview

Internal VC due diligence automation system for Crowley Capital. Transforms startup data into professional data room packages through automated analysis.

## Quick Start

```bash
/diligence init <company>     # Start new deal
/diligence analyze --all      # Run all analysis
/diligence risks              # Generate 11-risks scorecard
/diligence export             # Package data room
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE ORCHESTRATOR                     │
├─────────────────────────────────────────────────────────────────┤
│   SUBAGENTS              SKILLS              HOOKS              │
│   • financial-analyst    • saas-metrics      • on-file-upload   │
│   • captable-modeler     • cap-table-model   • on-metric-thresh │
│   • metrics-engine       • risk-framework    • on-analysis-done │
│   • customer-analyzer    • data-room-templ   • on-export        │
│   • risk-assessor        • austin-market                        │
│                          • data-audit                           │
│                          • data-room                            │
│                          • contract-review                      │
└─────────────────────────────────────────────────────────────────┘
```

## Key Files

| File | Purpose |
|------|---------|
| `CLAUDE.md` | This file - project overview |
| `QUICK-REFERENCE.md` | Commands and metrics cheat sheet |
| `ARCHITECTURE/system-design.md` | Technical architecture |
| `skills/*/SKILL.md` | Skill documentation |
| `PLANNING/*.md` | Implementation prompts |

## Skills (8)

| Skill | Purpose |
|-------|---------|
| **saas-metrics** | LTV, CAC, NRR, churn, cohorts |
| **cap-table-modeling** | Dilution, waterfalls, rounds |
| **risk-framework** | Tunguz 11-risks scoring |
| **data-room-templates** | Memos, dashboards, exports |
| **austin-market** | Regional context |
| **data-audit** | Meta Ads auditing for portfolio companies |
| **data-room** | Egnyte integration for secure document access |
| **contract-review** | Term sheets, agreements, legal diligence |

## Implementation Phases

| Phase | Focus |
|-------|-------|
| 0 | Foundation Setup |
| 1 | Core Skills (Metrics, Cap Table) |
| 2 | Subagent Integration & Hooks |
| 3 | Risk Assessment & Outputs |
| 4 | Polish & Austin Context |

## Data Room Structure

```
data-room/
├── raw/           # Uploaded files
│   ├── financials/
│   ├── customers/
│   ├── captable/
│   └── crm/
├── analysis/      # Generated analysis
└── output/        # Final deliverables
```

## MCP Integrations

| MCP Server | Purpose |
|------------|---------|
| **Egnyte** | Secure data room document access |
| **Pipeboard Meta** | Portfolio company ad account auditing |
| **Stape** | Server-side tracking assessment |

## Author

Built by Jordaaan for Crowley Capital — Austin, TX
