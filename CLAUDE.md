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
│                          • pdf-report-generator                 │
│                          • investor-matcher                     │
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

## Skills (16)

### Core Analysis
| Skill | Purpose |
|-------|---------|
| **saas-metrics** | LTV, CAC, NRR, churn, cohorts |
| **cap-table-modeling** | Dilution, waterfalls, rounds |
| **risk-framework** | Tunguz 11-risks scoring |
| **business-fin-analyst** | P&L analysis, burn rate, financial modeling |
| **investor-matcher** | Match startups to investors (40/40/20 algorithm) |

### Data & Documents
| Skill | Purpose |
|-------|---------|
| **data-room** | Egnyte integration for secure document access |
| **data-room-templates** | Memos, dashboards, exports |
| **contract-review** | Term sheets, agreements, legal diligence |
| **carta-integration** | Real-time cap tables, fund performance, 409A valuations |

### Report Generation
| Skill | Purpose |
|-------|---------|
| **diligence-report** | Compile analysis into PDF with Mermaid charts |
| **pdf-report-generator** | ReportLab-based PDF creation with branded styling |

### Context & Operations
| Skill | Purpose |
|-------|---------|
| **austin-market** | Regional context, investors, valuations |
| **data-audit** | Meta Ads auditing for portfolio companies |
| **phased-planning** | Implementation roadmaps, Claude Code prompts |
| **github-repo-creator** | Repository management |
| **organized-codebase-applicator** | Project structure templates |

## Report Generation

### PDF Report Generator
Professional PDF reports using ReportLab with:
- **Metric dashboards** — Color-coded KPI boxes
- **Risk scorecards** — Visual bar indicators
- **Tiered sections** — Priority-coded headers
- **Data tables** — Alternating rows, styled headers
- **Branded styling** — Crowley Capital colors

```python
from pdf_report_generator import InvestmentAssessmentReport

report = InvestmentAssessmentReport("Company Name", data, "output.pdf")
report.generate()
```

### Report Types
| Type | Pages | Use Case |
|------|-------|----------|
| Investment Assessment | 2-3 | IC review, deal evaluation |
| Investor Matches | 3 | Fundraising strategy |
| Diligence Summary | 8-10 | Full analysis compilation |
| LP Report | 4-5 | Portfolio updates |

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
│   ├── {company}/investment-assessment.md
│   └── {company}/investor-matches.md
└── output/        # Final deliverables
    ├── investment-memo.md
    ├── risk-scorecard.md
    ├── diligence-report.pdf
    └── investor-matches.pdf
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

## Brand Colors

```python
NAVY = '#1a365d'      # Headers, primary
GOLD = '#d69e2e'      # Accents, warnings
GREEN = '#38a169'     # Positive indicators
RED = '#e53e3e'       # Negative, high risk
GRAY = '#718096'      # Secondary text
LIGHT_GRAY = '#f7fafc' # Backgrounds
```

## Author

Built by Jordaaan for Crowley Capital — Austin, TX
