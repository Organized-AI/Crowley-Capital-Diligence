# Claude Code Web - Quick Start

## Step 1: Clone Repository

```bash
git clone https://github.com/Organized-AI/Crowley-Capital-Diligence.git
cd Crowley-Capital-Diligence
```

## Step 2: Install Dependencies

```bash
pip install pandas numpy openpyxl plotly tabulate jinja2 pyyaml
```

## Step 3: Copy This Prompt

---

## 🚀 LAUNCH PROMPT (Copy Everything Below)

```
Read CLAUDE.md and QUICK-REFERENCE.md to understand this VC diligence automation project for Crowley Capital.

This project has 11 skills in the skills/ directory:
- saas-metrics (LTV, CAC, NRR, churn)
- cap-table-modeling (dilution, waterfalls)
- risk-framework (Tunguz 11-risks)
- business-fin-analyst (P&L, burn rate)
- data-room (Egnyte integration)
- data-room-templates (memos, dashboards)
- contract-review (term sheets, legal)
- austin-market (regional context)
- data-audit (Meta Ads auditing)
- phased-planning (implementation)
- github-repo-creator (repo management)

Architecture is in ARCHITECTURE/system-design.md
Subagents are in .claude/agents/SUBAGENTS.md
Hooks are in .claude/hooks/HOOKS.md
Commands are in .claude/commands/diligence.md

For implementation, read PLANNING/phase-0-foundation.md and PLANNING/phase-1-core-skills.md

Confirm you've loaded the project context, then ask what I'd like to work on.
```

---

## Environment Variables (None Required for Core)

The core skills work without API keys. For MCP integrations:

```bash
# Optional - for Egnyte data room access
# (OAuth handled by MCP server)

# Optional - for Meta Ads auditing  
# (OAuth handled by Pipeboard MCP)

# Optional - for Stape server-side tracking
# STAPE_API_KEY=your_stape_api_key
```

---

## Quick Commands Once Running

```
/diligence init <company>     # Start new deal
/diligence analyze --all      # Run all analysis
/diligence risks              # Generate 11-risks scorecard
/diligence export             # Package data room
```

---

## Test With Sample Data

```bash
# Test metrics calculation
python skills/saas-metrics/scripts/calculate_metrics.py test-data/sample-revenue.csv

# Test financial analysis
python skills/business-fin-analyst/scripts/analyze_financials.py test-data/sample-revenue.csv --output md
```
