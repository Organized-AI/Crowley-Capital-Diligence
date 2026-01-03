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

### Core Analysis
| Skill | Purpose |
|-------|---------|
| **saas-metrics** | LTV, CAC, NRR, churn, cohort analysis |
| **cap-table-modeling** | Dilution scenarios, waterfalls, round modeling |
| **risk-framework** | Tunguz 11-risks scoring |
| **business-fin-analyst** | P&L analysis, burn rate, financial modeling |

### Data & Documents
| Skill | Purpose |
|-------|---------|
| **data-room** | Egnyte integration for secure document access |
| **data-room-templates** | Memos, dashboards, exports |
| **contract-review** | Term sheets, agreements, legal diligence |

### Context & Operations
| Skill | Purpose |
|-------|---------|
| **austin-market** | Regional context, investors, valuations |
| **data-audit** | Meta Ads auditing for portfolio companies |
| **phased-planning** | Implementation roadmaps, Claude Code prompts |

## Subagents

| Agent | Purpose |
|-------|---------|
| **financial-analyst** | Deep-dive financial analysis |
| **captable-modeler** | Cap table scenario modeling |
| **metrics-engine** | SaaS metrics calculation engine |
| **customer-analyzer** | Customer cohort and retention analysis |
| **risk-assessor** | 11-risks framework evaluation |

## Implementation Phases

| Phase | Description | Status |
|-------|-------------|--------|
| Phase 0 | Foundation Setup | Complete |
| Phase 1 | Core Skills (Metrics, Cap Table) | Complete |
| Phase 2 | Subagent Integration & Hooks | Complete |
| Phase 3 | Risk Assessment & Outputs | Complete |
| Phase 4 | Polish & Austin Context | Complete |

---

*Built by Jordaaan for Crowley Capital — Austin, TX*
