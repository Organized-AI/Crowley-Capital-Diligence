# Crowley Capital Diligence Tool

## Project Overview

Internal VC due diligence automation system for Crowley Capital. Transforms startup data into professional data room packages through automated analysis.

## Quick Start

```bash
/diligence init <company>     # Start new deal
/diligence analyze --all      # Run all analysis
/diligence risks              # Generate 11-risks scorecard
/diligence report             # Generate PDF report
/diligence export             # Package data room
```

## Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                    CLAUDE CODE ORCHESTRATOR                     │
├─────────────────────────────────────────────────────────────────┤
│   SUBAGENTS              SKILLS                 HOOKS           │
│   • financial-analyst    • saas-metrics         • on-file-upload│
│   • captable-modeler     • cap-table-modeling   • on-threshold  │
│   • metrics-engine       • risk-framework       • on-complete   │
│   • customer-analyzer    • data-room-templates  • on-export     │
│   • risk-assessor        • austin-market                        │
│                          • data-audit                           │
│                          • data-room                            │
│                          • contract-review                      │
│                          • business-fin-analyst                 │
│                          • carta-integration                    │
│                          • diligence-report                     │
│                          • phased-planning                      │
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

## Skills (13)

### Core Analysis
| Skill | Purpose |
|-------|---------|
| **saas-metrics** | LTV, CAC, NRR, churn, cohorts |
| **cap-table-modeling** | Dilution, waterfalls, rounds |
| **risk-framework** | Tunguz 11-risks scoring |
| **business-fin-analyst** | P&L analysis, burn rate, financial modeling |

### Data & Documents
| Skill | Purpose |
|-------|---------|
| **data-room** | Egnyte integration for secure document access |
| **data-room-templates** | Memos, dashboards, exports |
| **contract-review** | Term sheets, agreements, legal diligence |
| **carta-integration** | Real-time cap tables, fund performance, 409A valuations |
| **diligence-report** | PDF report generation with Mermaid visualizations |

### Context & Operations
| Skill | Purpose |
|-------|---------|
| **austin-market** | Regional context, investors, valuations |
| **data-audit** | Meta Ads auditing for portfolio companies |
| **phased-planning** | Implementation roadmaps, Claude Code prompts |
| **github-repo-creator** | Repository management |

## Report Generation

The diligence-report skill compiles all analysis into executive-ready PDFs:

```
┌─────────────────────────────────────────────────────────────────┐
│                    DILIGENCE REPORT                              │
├─────────────────────────────────────────────────────────────────┤
│  1. Executive Summary        Key metrics + recommendation       │
│  2. Financial Metrics        Revenue, unit economics, burn      │
│  3. Cap Table Analysis       Ownership, rounds, waterfall       │
│  4. Risk Assessment          11-Risks scorecard                 │
│  5. Market Context           Austin ecosystem, comparables      │
│  6. Appendix                 Full data tables                   │
└─────────────────────────────────────────────────────────────────┘
```

### Mermaid Chart Integration

Visual charts are generated via Mermaid Chart MCP:
- Ownership pie charts
- Revenue trend lines
- Risk radar diagrams
- Funding flow visualizations
- Unit economics flows

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
│   ├── metrics.json
│   ├── parsed_captable.json
│   └── cohorts.xlsx
└── output/        # Final deliverables
    ├── investment-memo.md
    ├── risk-scorecard.md
    ├── metrics-dashboard.html
    └── diligence-report.pdf
```

## MCP & API Integrations

| Integration | Purpose | Auth |
|-------------|---------|------|
| **Egnyte** | Secure data room document access | OAuth |
| **Pipeboard Meta** | Portfolio company ad account auditing | OAuth |
| **Stape** | Server-side tracking assessment | API Key |
| **Carta** | Cap tables, fund performance, valuations | OAuth 2.0 |
| **Mermaid Chart** | Visual diagram generation | MCP |

## Environment Variables

```bash
# Carta API (for carta-integration skill)
CARTA_CLIENT_ID=your_client_id
CARTA_CLIENT_SECRET=your_client_secret
CARTA_FIRM_ID=your_firm_id
CARTA_ENV=playground  # or production
```

## Author

Built by Jordaaan for Crowley Capital — Austin, TX
